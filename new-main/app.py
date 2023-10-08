from flask import Flask, render_template
import os

import json
import pandas as pd
import plotly.express as px 


app = Flask(__name__, template_folder='templates')
@app.route('/')

@app.route("/")
def home():
    with open("Methane Metadata.json", "r") as f:
        data_json = f.read()

    result = json.loads(data_json)
    
    max_latitude = []
    max_longitude = []
    max_plume_list = []
    utc_time_list = []


    for data in result["features"]:
        if data["geometry"]["type"] == "Point":
            lati = data["properties"]["Latitude of max concentration"]
            long = data["properties"]["Longitude of max concentration"]
            max_plume = data["properties"]["Max Plume Concentration (ppm m)"]
            time = data["properties"]["UTC Time Observed"]
            max_latitude.append(lati)
            max_longitude.append(long)
            max_plume_list.append(max_plume)
            utc_time_list.append(time)

    print(max_latitude[0], max_longitude[0], max_plume_list[0], utc_time_list[0])

    data_air = pd.DataFrame({
        "Latitude(degree)": max_latitude,
        "Longitude(degree)": max_longitude,
        "Max Methane Emit(ppm)": max_plume_list,
        "UTC Time Observed": utc_time_list
    })

    data_air
    result = json.loads(data_json)
   
    map_fig = px.scatter_mapbox(data_air, 
                            lat = data_air['Latitude(degree)'], 
                            lon = data_air['Longitude(degree)'],
                            zoom = 3,
                            color = data_air['Max Methane Emit(ppm)'],
                            size = data_air['Max Methane Emit(ppm)'],
                            height = 900,
                            width = 1200)

    map_fig.update_layout(mapbox_style="open-street-map")
    map_fig.update_layout(margin={"r":0, "t":50, "l":0, "b":10})

    map_fig_html = map_fig.to_html(map_fig)
    return render_template("data.html", map_fig_html=map_fig_html)
    


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')