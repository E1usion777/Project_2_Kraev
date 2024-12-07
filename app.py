from flask import Flask, request, render_template
import requests

app = Flask(__name__)

API_KEY = 'flfzTb3fcLHgaYB5sov7F0A3A78MnFn1'


def check_bad_weather(temperature, wind_speed, precipitation_probability):
    """
    Функция для оценки погодных условий.
    """


    if temperature < 0 or temperature > 35:
        return False
    if wind_speed > 50:
        return False
    if precipitation_probability > 70:
        return False
    return True


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def get_weather():
    start_city = request.form['start_city']
    end_city = request.form['end_city']

    #Определяем ключ города по его названию
    location_url_start = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={start_city}'
    location_response_start = requests.get(location_url_start)

    if location_response_start.status_code != 200:
        return render_template('index.html', error="Не удалось получить данные о местоположении начального города")

    location_data_start = location_response_start.json()
    if not location_data_start:
        return render_template('index.html', error="Начальный город не найден")

    start_location_key = location_data_start[0]['Key']

    weather_url_start = f'http://dataservice.accuweather.com/currentconditions/v1/{start_location_key}?apikey={API_KEY}&details=true'
    weather_response_start = requests.get(weather_url_start)

    if weather_response_start.status_code != 200:
        return render_template('index.html', error="Не удалось получить данные о погоде для начального города")

    weather_data_start = weather_response_start.json()
    if not weather_data_start:
        return render_template('index.html', error="Данные о погоде недоступны для начального города")

    current_conditions_start = weather_data_start[0]

    temperature_start = current_conditions_start['Temperature']['Metric']['Value']
    wind_speed_start = current_conditions_start['Wind']['Speed']['Metric']['Value']
    precipitation_probability_start = current_conditions_start['PrecipitationSummary']['Precipitation']['Metric']['Value']

    if precipitation_probability_start is None:
        precipitation_probability_start = 'Нет данных'

    good_weather_start = check_bad_weather(temperature_start, wind_speed_start, precipitation_probability_start)

    # Получаем ключ для конечного города
    location_url_end = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={end_city}'
    location_response_end = requests.get(location_url_end)

    if location_response_end.status_code != 200:
        return render_template('index.html', error="Не удалось получить данные о местоположении конечного города")

    location_data_end = location_response_end.json()
    if not location_data_end:
        return render_template('index.html', error="Конечный город не найден")

    end_location_key = location_data_end[0]['Key']

    weather_url_end = f'http://dataservice.accuweather.com/currentconditions/v1/{end_location_key}?apikey={API_KEY}&details=true'
    weather_response_end = requests.get(weather_url_end)

    if weather_response_end.status_code != 200:
        return render_template('index.html', error="Не удалось получить данные о погоде для конечного города")

    weather_data_end = weather_response_end.json()

    if not weather_data_end:
        return render_template('index.html', error="Данные о погоде недоступны для конечного города")

    current_conditions_end = weather_data_end[0]

    temperature_end = current_conditions_end['Temperature']['Metric']['Value']
    wind_speed_end = current_conditions_end['Wind']['Speed']['Metric']['Value']
    precipitation_probability_end = current_conditions_end['PrecipitationSummary']['Precipitation']['Metric']['Value']

    if precipitation_probability_end is None:
        precipitation_probability_end = 'Нет данных'

    good_weather_end = check_bad_weather(temperature_end, wind_speed_end, precipitation_probability_end)

    # Логика принятия решения о походе
    if good_weather_start and good_weather_end:
        message = "Время идти в путешествие!"
    else:
        message = "Не самое подходящее время для путешествий."

    return render_template('index.html',
                           start_city=start_city,
                           temperature_start=temperature_start,
                           wind_speed_start=wind_speed_start,
                           precipitation_probability_start=precipitation_probability_start,
                           end_city=end_city,
                           temperature_end=temperature_end,
                           wind_speed_end=wind_speed_end,
                           precipitation_probability_end=precipitation_probability_end,
                           message=message)


if __name__ == '__main__':
    app.run(debug=True)