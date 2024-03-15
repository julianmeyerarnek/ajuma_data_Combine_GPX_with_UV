import datetime
import gpxpy
import gpxpy.gpx
import pytz
import sys
from simplekml import Kml

colors=["ff110011", "ff330022", "ff550033", "ff770044", "ff990055", "ffaa0066", "ffcc0077", "ffee0088", "ffff0099", "ff0000aa", "ff0000ff"]

def parse_uvbg (infile):

    uvtrack = []

    f = open (infile, "r")
    lines = f.readlines ()
    f.close()

    for l in lines:
        xtime_str=(int(l.split(",")[0]))/1000.0
        xtime_dt = datetime.datetime.fromtimestamp (xtime_str)
        xtime_dt -= datetime.timedelta (0, 2 * 60 * 60) # CEST > UTC
        xuvi = float(l.split(",")[1])

        if not "xtime_m1_dt" in locals():
            xtime_m1_dt = xtime_dt

        if not xtime_m1_dt == xtime_dt:
            uvtrack.append({"time": xtime_dt.replace(tzinfo=pytz.UTC), "uvi": xuvi})

        xtime_m1_dt = xtime_dt

    return (uvtrack)


gpx_filename = '2023-06-18_13-43.gpx'
uvbg_filename= 'share_csv_1687088477889.csv'

gpx = gpxpy.parse(open(gpx_filename), "r")

geotrack = []
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            geotrack.append({"time": point.time, "lon": point.longitude, "lat": point.latitude, "elevation": point.elevation, "uvi": -1})
#           print('Point at ({0},{1},{2}) -> {3}'.format(point.time, point.latitude, point.longitude, point.elevation))

uvtrack = parse_uvbg (uvbg_filename)

for g in geotrack:
    xgeotime = g["time"]

    xdeltat = []
    for uv in uvtrack:
        xdeltat.append (abs(uv["time"] - xgeotime))

    xmindeltat = min (xdeltat)
    i = xdeltat.index (xmindeltat)

    g["uvi"] = uvtrack[i]["uvi"]

# print (geotrack)

for g in geotrack:
    print (g["lon"], g["lat"], g["elevation"], g["uvi"])

# sys.exit()

kml = Kml()
fol = kml.newfolder(name="A Folder")
for g in geotrack:
    pnt = fol.newpoint(name="{0}".format(int(g["uvi"])), coords=[(g["lon"],g["lat"])])
    uv_index = int(g["uvi"])
    if uv_index > 11: uv_index = 11
    print (uv_index)
    pnt.style.iconstyle.color = colors[uv_index] # float(float(uv_index) / 3.0)
#   pnt.style.labelstyle.color = colors[uv_index]

kml.save("output.kml")
