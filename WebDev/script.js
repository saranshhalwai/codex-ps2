const apiKey = 'b805419fdd67d5e6eca1c1c57be612ec';
const searchBtn = document.getElementById('search-btn');
const locationInput = document.getElementById('location');
const weatherResult = document.getElementById('weather-result');

searchBtn.addEventListener('click', () => {
    const location = locationInput.value.trim();
    if (!location) {
        alert('Please enter a location!');
        return;
    }
    fetchWeather(location);
});

async function fetchWeather(location) {
    try {
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${location}&units=metric&appid=${apiKey}`);
        if (!response.ok) {
            throw new Error('Location not found');
        }
        const data = await response.json();
        displayWeather(data);
    } catch (error) {
        alert(error.message);
    }
}

function displayWeather(data) {
    const { name, main: { temp, humidity }, weather, wind: { speed } } = data;
    weatherResult.innerHTML = `
        <h2>Weather in ${name}</h2>
        <p><strong>Temperature:</strong> ${temp}°C</p>
        <p><strong>Humidity:</strong> ${humidity}%</p>
        <p><strong>Wind Speed:</strong> ${speed} m/s</p>
        <p><strong>Condition:</strong> ${weather[0].description}</p>
    `;
}
