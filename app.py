from flask import Flask, render_template, request, redirect
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Weather(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    city = db.Column(db.String(100), nullable = False)
    # Below is given how we can store array in database
    temp = db.Column(db.Text, nullable = False)        # It will store data in json form
    weather = db.Column(db.String(100), nullable = False)
    country = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"{self.city} - {self.temp} - {self.weather} - {self.country}"



@app.route('/', methods = ['GET', 'POST'])
def home():
    api = "d068d7a8dff8a926b18a4323abd4b4dc"
    weather = None

    if (request.method == 'POST'):
        
        cityname = request.form['cityname']
        print(cityname)
        url = f"https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid={api}"
        
        response = requests.get(url)
        if (response.status_code == 200):
            weather_details = response.json()
            print(weather_details)

            city = weather_details['name']
            
            # fahrenheit = weather_details['main']['temp']
            # temp = (fahrenheit - 32) * 5 // 9

            temp = weather_details['main']['temp']
            day = weather_details['weather'][0]['main']
            country = weather_details['sys']['country']

            # weather = Weather(city = city ,temp = temp,  weather = day, country = country)
            weather = Weather(city = city ,temp = temp,  weather = day, country = country)
            db.session.add(weather)
            db.session.commit()

            return render_template('index.html', weather = weather)        

    return render_template("index.html", weather = weather)


@app.route('/history')
def history():
    weather = Weather.query.all()
    return render_template('history.html', weather = weather)

@app.route('/delete/<int:sno>')
def delete(sno):
    weather = Weather.query.filter_by(sno = sno).first()
    db.session.delete(weather)
    db.session.commit()
    return redirect('/history')



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)