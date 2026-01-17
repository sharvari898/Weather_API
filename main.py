from flask import Flask,render_template
import pandas as pd


app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows = 17)
station = stations[["STAID","STANAME                                 "]]
@app.route("/")
def home():
    return render_template("home.html",data = station.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station,date):
    df = pd.read_csv("data_small/TG_STAID" + str(station).zfill(6)+ ".txt", skiprows = 20 ,
                     parse_dates = ["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].min().squeeze() / 10
    return {
        "station" : station,
        "date" : date,
        "temperature" : temperature
    }
@app.route("/api/v1/<station>")
def all_station(station):
    filename = pd.read_csv("data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20,
                     parse_dates=["    DATE"])
    return filename.to_dict(orient = "records")
@app.route("/api/v1/yearly/<station1>/<year>")
def yearly(station1,year):
    filename = pd.read_csv("data_small/TG_STAID" + str(station1).zfill(6) + ".txt", skiprows=20)
    filename["    DATE"] = filename["    DATE"].astype(str)
    result = filename["    DATE"].str.startswith(str(year)).to_dict()
    print(result)
    return result
if __name__ == "__main__":
    app.run(debug=True)