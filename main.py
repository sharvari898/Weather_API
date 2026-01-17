from flask import Flask,render_template
import pandas as pd


app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows = 17)
station = stations[["STAID","STANAME                                 "]]


@app.route("/")
def home():
    """
        return home.html page
    :return:
    """

    return render_template("home.html",data = station.to_html())


@app.route("/api/v1/<station>/<date>")
def station_data(station,date):
    """
        return data for specific station for specific year
        :param station:
        :return:
        """
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
    """
    return data for specific station for all years
    :param station:
    :return:
    """
    filename = pd.read_csv("data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20,
                     parse_dates=["    DATE"])
    return filename.to_dict(orient = "records")


@app.route("/api/v1/yearly/<station1>/<year>")
def yearly(station1,year):
    """
    to return all data for specific station for mentioned year
    :param station1:
    :param year:
    :return: dict
    """
    filename = pd.read_csv("data_small/TG_STAID" + str(station1).zfill(6) + ".txt", skiprows=20)
    filename["    DATE"] = filename["    DATE"].astype(str)
    result = filename[filename["    DATE"].str.startswith(str(year))].to_dict(orient = "records")
    return result

if __name__ == "__main__":
    app.run(debug=True)