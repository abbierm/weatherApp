var dayWeatherIcons = {"clear": "sunny", "few-clouds": "sunny", "scattered-clouds": "cloudy", "shower-rain": "rainy", "rain": "rainy", "thunderstorm": "thunderstorm", "clear-sky": "sunny", "broken-clouds": "cloudy", "snow": "snow", "mist": "menu", "overcast-clouds": "cloudy", "haze": "menu", "light-rain": "rainy", "moderate-rain": "rainy", "heavy-intensity-rain": "rainy"
};

var nightWeatherIcons = {"clear": "moon", "few-clouds": "cloudy-night", "scattered-clouds": "cloudy-night", "shower-rain": "umbrella", "rain": "umbrella", "thunderstorm": "thunderstorm", "clear-sky": "moon", "broken-clouds": "cloudy-night", "snow": "snow", "mist": "menu", "cloudy": "cloudy-night", "haze": "menu", "overcast-clouds": "cloudy", "light-rain": "umbrella", "moderate-rain": "umbrella", "heavy-intensity-rain": "rainy"};




// document.addEventListener('DOMContentLoaded', () => {
//     // gets the correct 'icon' to appear
//     const iconInfo = document.getElementById("icon-name");
//     const hourInfo = document.getElementById("hours");
//     if (iconInfo) {
//         var key = iconInfo.dataset.name;

//         // Doing this until I've made all of the icons
//         var iconName;
//         if (homeMadeIconsDay[key]) {
//             iconName = homeMadeIconsDay[key];
//         }
//         else {
//             var iconName = dayWeatherIcons[key];
//             var hours = hourInfo.dataset.name;
//             if (hours > 20 || hours < 6) {
//                 iconName = nightWeatherIcons[key];
//             }     
//             else {
//                 iconName = dayWeatherIcons[key];
//             }
//         }    
//         document.getElementById("icon").setAttribute("name", iconName);
//     }
// });
