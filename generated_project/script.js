// Weather App Demo
document.getElementById('search-btn').addEventListener('click', searchWeather);
document.getElementById('city-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchWeather();
});

function searchWeather() {
    const city = document.getElementById('city-input').value;
    if (!city) return;
    
    // Demo weather data
    const demoWeather = {
        'New York': { temp: 22, desc: 'Sunny', icon: '☀️' },
        'London': { temp: 15, desc: 'Cloudy', icon: '☁️' },
        'Tokyo': { temp: 28, desc: 'Partly Cloudy', icon: '⛅' },
        'Paris': { temp: 18, desc: 'Rainy', icon: '🌧️' }
    };
    
    const weather = demoWeather[city] || { temp: 20, desc: 'Clear', icon: '☀️' };
    
    document.getElementById('city-name').textContent = city;
    document.getElementById('temperature').textContent = weather.temp + '°C';
    document.getElementById('description').textContent = weather.desc;
    document.querySelector('.weather-icon').textContent = weather.icon;
}