"""
Real-Time Indian Weather App (No API Key Needed)
------------------------------------------------
Powered by Open-Meteo API - Free & Accurate Weather Data
Professional clean output using Rich library (No Emojis)
"""

import requests
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()

def get_coordinates(city: str):
    """Get latitude, longitude, and full city name using Open-Meteo's geocoding"""
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    
    try:
        response = requests.get(geocode_url)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("results"):
            return None
        
        result = data["results"][0]
        return {
            "lat": result["latitude"],
            "lon": result["longitude"],
            "city": f"{result['name']}, {result.get('country', 'India')}".strip(", ")
        }
    
    except requests.RequestException:
        console.print(Panel("[red]Network error: Please check your internet connection.[/red]",
                            title="Connection Issue", border_style="red"))
        return None


def get_weather(lat: float, lon: float):
    """Fetch current weather data from Open-Meteo"""
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        f"&timezone=Asia/Kolkata"
    )
    
    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        data = response.json()["current"]
        
        # Weather description without emojis
        codes = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            61: "Light rain", 63: "Moderate rain", 65: "Heavy rain",
            71: "Light snow fall", 73: "Snow fall", 75: "Heavy snow fall",
            80: "Light rain showers", 81: "Rain showers", 82: "Violent rain showers",
            95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Heavy thunderstorm"
        }
        
        description = codes.get(data["weather_code"], "Unknown weather conditions")
        
        return {
            "temperature": data["temperature_2m"],
            "humidity": data["relative_humidity_2m"],
            "wind_speed": data["wind_speed_10m"],
            "description": description
        }
    
    except requests.RequestException:
        console.print(Panel("[red]Failed to fetch weather data.[/red]",
                            title="API Error", border_style="red"))
        return None


def main():
    console.print(Panel(
        "[bold cyan]Real-Time Indian Weather App[/bold cyan]\n"
        "[dim]No API Key Required | Accurate Data for All Indian Cities[/dim]",
        title="Welcome",
        border_style="bright_blue",
        box=box.DOUBLE
    ))
    
    while True:
        console.print()
        city = console.input("[bold green]Enter city name[/bold green] (e.g. Mumbai, Delhi) or type [bold red]'quit'[/bold red] to exit: ").strip()
        
        if city.lower() == "quit":
            console.print("\n[yellow]Thank you for using the Weather App![/yellow]")
            break
        
        if not city:
            console.print("[red]Please enter a valid city name.[/red]")
            continue
        
        console.print("[dim]Fetching weather data...[/dim]")
        
        coords = get_coordinates(city)
        if not coords:
            console.print(Panel(
                f"[red]City '{city}' not found.[/red]\n"
                "Tip: Try full names like 'New Delhi', 'Bengaluru', 'Kolkata'",
                title="City Not Found",
                border_style="red",
                box=box.ROUNDED
            ))
            continue
        
        weather = get_weather(coords["lat"], coords["lon"])
        if weather:
            console.print(Panel(
                f"[bold blue]Location:[/bold blue] {coords['city']}\n\n"
                f"[bold magenta]Temperature:[/bold magenta] {weather['temperature']} °C\n"
                f"[bold cyan]Humidity:[/bold cyan] {weather['humidity']} %\n"
                f"[bold yellow]Wind Speed:[/bold yellow] {weather['wind_speed']} km/h\n"
                f"[bold green]Conditions:[/bold green] {weather['description']}",
                title="Current Weather",
                border_style="bright_green",
                box=box.ROUNDED
            ))


if __name__ == "__main__":
    main()