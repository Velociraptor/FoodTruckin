#!flask/bin/python

from flask import Flask, render_template, request, url_for
import urllib2, json

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():

    center = 'San Francisco'
    food_type = 'all'
    if request.method == 'POST':
        in_center = request.form['center']
        in_food_type = request.form['food_type']
        if in_center != '':
            center = in_center
        if in_food_type != '':
            food_type = in_food_type

    food_trucks = get_trucks(food_type)

    (latitude, longitude) = get_lat_lng(center)
    return render_template('index.html',
        title = "Food Truckin'",
        latitude = latitude,
        longitude = longitude,
        trucks = food_trucks,
        center_fill = center,
        food_fill = food_type)

def get_lat_lng(address):
    (latitude,longitude) = (37.7833, -122.4167)
    address = urllib2.quote(address + ' San Francisco') # cross streets entered should now localize to SF rather than other places
    url='http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false' % address
    response = urllib2.urlopen(url).read()
    try:
        response_ll = json.loads(response)['results'][0]['geometry']['location']
        latitude = response_ll['lat']
        longitude = response_ll['lng']
    except:
        pass
    return (latitude,longitude)

def get_trucks(food_type):
    if food_type == 'all':
        response = urllib2.urlopen('https://data.sfgov.org/resource/rqzj-sfat.json')
        trucks = json.loads(response.read())
        truck_jsons = [] # Having issues with the json in javascript so just parsing what is needed here for now
        for truck in trucks:
            try:
                name = truck['applicant']
                item = truck['fooditems']
                lat = truck['latitude']
                lng = truck['longitude']
                truck_json = '{"name":"%s","item":"%s","lat":"%s","lng":"%s"}' %(name,item,lat,lng)
                truck_jsons.append(str(truck_json))
            except:
                pass
        return truck_jsons
    else:
        response = urllib2.urlopen('https://data.sfgov.org/resource/rqzj-sfat.json')
        trucks = json.loads(response.read())
        truck_jsons = []
        for truck in trucks:
            try:
                name = truck['applicant']
                item = truck['fooditems']
                if food_type.lower() not in item.lower():
                    continue
                lat = truck['latitude']
                lng = truck['longitude']
                truck_json = '{"name":"%s","item":"%s","lat":"%s","lng":"%s"}' %(name,item,lat,lng)
                truck_jsons.append(str(truck_json))
            except:
                pass
        return truck_jsons

if __name__ == '__main__':
    app.run()