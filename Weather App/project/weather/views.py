from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    # Default city is Chennai if no input is given
    city = request.POST.get('city', 'Chennai')  

    # OpenWeather API for weather details
    WEATHER_API_KEY = "1b9e6813e0f847495111c5b0b30b6c75"  # Use a valid API Key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
    PARAMS = {'units': 'metric'}

    # Google Custom Search API for city image
    GOOGLE_API_KEY = "AIzaSyCs5aU1qzY4kSFg87_GxwsPx_2cL0lkk7o"  # Add your API Key
    SEARCH_ENGINE_ID = "c172c149e43904a09"  # Add your Search Engine ID

    query = f"{city} 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = "image"
    city_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    # Default image URL in case API fails
    image_url = "https://via.placeholder.com/1920x1080?text=No+Image+Available"

    try:
        # Fetch image URL
        response = requests.get(city_url).json()
        if response.status_code == 200:
            data = response.json()
            search_items = data.get("items")
            if search_items and len(search_items) > 1:
                image_url = search_items[1]["link"]

    except Exception as e:
        print("Error fetching image:", e)

    try:
        # Fetch weather data
        response = requests.get(url, params=PARAMS)
        if response.status_code == 200:
            data = response.json()
            description = data["weather"][0]["description"]
            icon = data["weather"][0]["icon"]
            temp = data["main"]["temp"]
            day = datetime.date.today()

            return render(
                request,
                "weatherapp/index.html",
                {
                    "description": description,
                    "icon": icon,
                    "temp": temp,
                    "day": day,
                    "city": city,
                    "exception_occurred": False,
                    "image_url": image_url,
                },
            )

    except KeyError:
        messages.error(request, "Entered data is not available in the API")

    # Handle errors by showing a default message
    return render(
        request,
        "weatherapp/index.html",
        {
            "description": "clear sky",
            "icon": "01d",
            "temp": 25,
            "day": datetime.date.today(),
            "city": "Chennai",
            "exception_occurred": True,
            "image_url": image_url,
        },
    )
