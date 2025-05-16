
let celsius = true;


function convertToCelsius(temp) {
    return Math.round((temp - 32) * (5 / 9));
}

function convertToFahrenheit(temp) {
    return Math.round((temp * 1.8) + 32);
}

function convertToPsi(pressure) {
    var psiPressure = pressure * .029529980;
    return psiPressure.toFixed(2);
}

function convertToMph(speed) {
    return Math.round((speed * .621371));
}



function toggleToCelsius() {
    
    if (!celsius) {
        let currentTemps = document.querySelectorAll(".temp");
        for (let el of currentTemps) {
            let newTemp = convertToCelsius(Number(el.innerHTML));
            el.innerHTML = newTemp;
        }
        
        let currentUnits = document.querySelectorAll(".units");
        for (let unit of currentUnits) {
            unit.innerHTML = '°C';
        }
        celsius = true;

        // 
        let current = document.getElementById("large-celsius"), old = document.getElementById("large-fahrenheit");
        current.classList.replace("inactive", "active");
        old.classList.replace("active", "inactive");

        // Pressure
        let pressureElement = document.getElementById("pressure");
        let p = pressureElement.dataset.name;
        pressureElement.innerHTML = p + ' mbar';

        // windspeed
        let windSpeedElement = document.getElementById("wind-speed");
        let s = Math.Round(windSpeedElement.dataset.name) + ' kph';
        windSpeedElement.innerHTML = s;
    }
}

function toggleToFahrenheit() {
    
    if (celsius) {
        let currentTemps = document.querySelectorAll(".temp");
        for (let el of currentTemps) {
            let newTemp = convertToFahrenheit(Number(el.innerHTML));
            el.innerHTML = newTemp;
        }
        let currentUnits = document.querySelectorAll(".units");
        for (let unit of currentUnits) {
            unit.innerHTML = '°F';
        }
        celsius = false;
        let cur = document.getElementById("large-fahrenheit"), old = document.getElementById("large-celsius");
        cur.classList.replace("inactive", "active");
        old.classList.replace("active", "inactive");

        // change the pressure
        let pressureElement = document.getElementById("pressure");
        let p = pressureElement.dataset.name;
        pressureElement.innerHTML = convertToPsi(p) + ' in';

        // change windspeed
        let windSpeedE = document.getElementById("wind-speed");
        let s = windSpeedE.dataset.name;
        windSpeedE.innerHTML = convertToMph(s) + ' mph';
    }
}