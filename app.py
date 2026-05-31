from flask import Flask, render_template, request
import requests
app =Flask(__name__)
def weatherimg(code):
    if code ==0:
        return "sunny.png"
    elif code in [1, 2, 3]:
        return "cloudy.png"
    elif code in [80,81]:
        return "eclipse.png"
    elif code in [45, 48]:
        return "fog.png"
    elif code in [51,52,53,54,56,57,58,59,60,61]:
        return "rain.png"
    elif code in [71, 73, 75,77,85,86]:
        return "snow.png"
 
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/weather")
def weather():
    lat =request.args.get("lat")
    lon =request.args.get("lon")
    print("LAT:", lat)
    print("LON:", lon)
    
    if not lat or not lon:
        return render_template("index.html", error="위치 정보 없음")
    
    url =f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response =requests.get(url)
    data =response.json()
    print("DATA:", data)
    if "current_weather" not in data:
        return render_template("index.html", error="날씨 데이터 없음")

    code =data["current_weather"]["weathercode"]

    weather ={
        "temp": data["current_weather"]["temperature"],
        "windspeed": data["current_weather"]["windspeed"],
        "weathercode": code,
        "image": weatherimg(code)
    }
    print(weather["temp"])
    print(weather["windspeed"])
    print(weather["image"])
    return render_template("index.html", weather=weather)
if __name__=="__main__":
     app.run(debug=True)