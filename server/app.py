from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///environmental_data.db'
db = SQLAlchemy(app)

class EnvironmentalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    air_quality = db.Column(db.Float, nullable=False)

@app.route('/data', methods=['GET'])
def get_data():
    data = EnvironmentalData.query.all()
    return jsonify([{
        'id': d.id,
        'temperature': d.temperature,
        'humidity': d.humidity,
        'air_quality': d.air_quality
    } for d in data])

@app.route('/data', methods=['POST'])
def add_data():
    data = request.json
    new_data = EnvironmentalData(
        temperature=data['temperature'],
        humidity=data['humidity'],
        air_quality=data['air_quality']
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Data added successfully'}), 201

def fetch_environmental_data():
    # Example API calls (replace with actual API URLs and keys)
    weather_response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=City&appid=YOUR_API_KEY')
    air_quality_response = requests.get('http://api.airvisual.com/v2/city?city=City&key=YOUR_API_KEY')

    if weather_response.status_code == 200 and air_quality_response.status_code == 200:
        weather_data = weather_response.json()
        air_quality_data = air_quality_response.json()

        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        air_quality = air_quality_data['data']['current']['pollution']['aqius']

        new_data = EnvironmentalData(
            temperature=temperature,
            humidity=humidity,
            air_quality=air_quality
        )
        db.session.add(new_data)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        fetch_environmental_data()
    app.run(debug=True)

