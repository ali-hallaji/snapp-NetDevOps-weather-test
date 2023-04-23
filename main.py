import httpx
from datetime import timezone, datetime

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBasicCredentials

from config import settings
from model import Weather, User
from utils import get_db, get_current_user, get_user, create_access_token

app = FastAPI()


@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)

    if not user or form_data.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/v1/weather")
async def get_weather(city: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    url = f"{settings.WEATHER_API_URL}?q={city}&appid={settings.WEATHER_API_KEY}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {"detail": f"City '{city}' not found."}
            else:
                raise HTTPException(status_code=404, detail=e) from e

        data = response.json()

    weather = {
        "city": city,
        "Temp": data["main"]["temp"],
        "Hum": data["main"]["humidity"]
    }
    db_weather = Weather(
        city=city,
        temperature=weather["Temp"],
        humidity=weather["Hum"],
        time=datetime.now(timezone.utc)
    )

    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return weather


@app.get("/v1/weather/history")
async def get_weather_history(
    offset: int=0,
    limit: int=10,
    db: Session=Depends(get_db), 
    current_user: User=Depends(get_current_user)
    ):
    if weather_data := db.query(Weather).offset(offset).limit(limit).all():
        return [
            {
                "city": weather.city, "temperature": weather.temperature,
                "humidity": weather.humidity, "time": weather.time
            } for weather in weather_data
        ]
    else:
        raise HTTPException(status_code=404, detail="No weather data found")