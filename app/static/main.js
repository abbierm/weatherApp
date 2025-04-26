var dayWeatherIcons = {"clear": "sunny", "few-clouds": "sunny", "scattered-clouds": "cloudy", "shower rain": "rainy", "rain": "rainy", "thunderstorm": "thunderstorm", "clear sky": "sunny", "broken-clouds": "cloudy", "snow": "snow", "mist": "menu",
    "overcast-clouds": "cloudy", "haze": "menu"
}

var nightWeatherIcons = {"clear": "moon", "few-clouds": "cloudy-night", "scattered-clouds": "cloudy-night", "shower rain": "umbrella", "rain": "umbrella", "thunderstorm": "thunderstorm", "clear sky": "moon", "broken-clouds": "cloudy-night", "snow": "snow", "mist": "menu"}




document.addEventListener('DOMContentLoaded', () => {
    // gets the correct 'icon' to appear
    const iconInfo = document.getElementById("icon-name");
    if (iconInfo) {
        const key = iconInfo.dataset.name;
        const iconName = dayWeatherIcons[key];
        if (iconName) {
            document.getElementById("icon").setAttribute("name", iconName);
        }
    }
});
