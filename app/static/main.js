
let celsius = true;


function convertToCelsius(temp) {
    return Math.round((temp - 32) * (5 / 9));
}

function convertToFahrenheit(temp) {
    return Math.round((temp * 1.8) + 32);
}


function toggleTempUnits() {
    var currentTemps = document.querySelectorAll(".temp");
    var currentUnits = document.querySelectorAll(".units")
    if (!celsius) {
        currentTemps.forEach((el, index) => {
            var newTemp = convertToCelsius(Number(el.innerHTML));
            el.innerHTML = newTemp;
        })
        currentUnits.forEach((units, index) => {
            units.innerHTML = '°C';
        })
        celsius = true;
    }
    else {
        currentTemps.forEach((el, i) => {
            var temp = convertToFahrenheit(Number(el.innerHTML));
            el.innerHTML = temp;
        })
        currentUnits.forEach((un, i) => {
            un.innerHTML ='°F';
        })
        celsius = false;
    }
    
}