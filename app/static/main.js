 let units;
 if (localStorage.getItem("units") == null) {
   units = "metric";
 }
 else {
   units = localStorage.getItem("units");
 }

 function toFahrenheit(temp) {
    return Math.round((temp * 1.8) + 32);
 }

 function toInHg(p) {
    let v = .02953;
    return Math.round(p * v);
 }

 function toMph(s) {
    return Math.round(s / 1.609344);
 }


// Loads all the scripts to be 
function switchToImperial() {
   // converts the temps
   let currentTemps = document.querySelectorAll(".temp");
   for (let t of currentTemps) {
      t.innerHTML =`${toFahrenheit(Number(t.dataset.name))} °F`;
   }
  
   // Converts the pressure + units
   let currentPressure = document.querySelectorAll(".pressure");
   for (let p of currentPressure) {
      p.innerHTML =`${toInHg(Number(p.dataset.name))} in`;
   }

   // converts windspeed
   let currentWindVelo = document.querySelectorAll(".wind-velo");
   for (let w of currentWindVelo) {
      w.innerHTML = `${Number(toMph(w.dataset.name))} mph`;
   }

   // Changes toggle button
   document.getElementById("top-r2-lc-degree-toggle-button").innerHTML = '°C';
}

function switchToMetric() {
   let currentTemps = document.querySelectorAll(".temp");
   for (let t of currentTemps) {
      let temp = t.dataset.name;
      t.innerHTML = `${temp} °C`;
   }
   
   let currentPresssure = document.querySelectorAll(".pressure"); 
   for (let p of currentPresssure) {
      p.innerHTML = `${p.dataset.name} mb`;
   }

   let currentWindVelo = document.querySelectorAll(".wind-velo");
   for (let w of currentWindVelo) {
      w.innerHTML = `${w.dataset.name} kph`;
   }

   document.getElementById("top-r2-lc-degree-toggle-button").innerHTML = '°F';

}

document.addEventListener("DOMContentLoaded", () => {
      if (units == "imperial") {
         switchToImperial();
      }
      else {
         switchToMetric();
      }
})

function toggleUnits() {
   if (localStorage.getItem("units") == "metric") {
      switchToImperial();
      localStorage.setItem("units", "imperial");
   }
   else {
      switchToMetric();
      localStorage.setItem("units", "metric");
   }
 }


function scrollCarousel(direction) {
   const carousel = document.getElementById("hours-carousel");
   const scrollAmount = 220;
   carousel.scrollBy({"left": direction * scrollAmount, "behavior": "smooth"});
}