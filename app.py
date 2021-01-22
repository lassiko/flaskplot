from flask import Flask, Markup, render_template

import xml.etree.ElementTree as ET
import collections
import sys
sys.path.append('/home/site/wwwroot')
import requests
import datetime as dt

app = Flask(__name__)

@app.route('/')

def line():

    x1 = []
    y1 = []
    x2 = []
    y2 = []

    weather_vt51_url = "http://opendata.fmi.fi/wfs?request=getFeature&storedquery_id=livi::observations::road::multipointcoverage&fmisid=100013&parameters=TA,RH,TD,WS,WD,WG"
    data = requests.get(weather_vt51_url)
    root = ET.fromstring(data.text)
    for member in root.iter('{http://www.opengis.net/wfs/2.0}member'):
        for GridSeriesObservation in member.iter('{http://inspire.ec.europa.eu/schemas/omso/3.0}GridSeriesObservation'):
            for result in GridSeriesObservation.iter('{http://www.opengis.net/om/2.0}result'):
                for MultiPointCoverage in result.iter('{http://www.opengis.net/gmlcov/1.0}MultiPointCoverage'):
                    for domainSet in MultiPointCoverage.iter('{http://www.opengis.net/gml/3.2}domainSet'):
                        for SimpleMultiPoint in domainSet.iter('{http://www.opengis.net/gmlcov/1.0}SimpleMultiPoint'):
                            for positions in SimpleMultiPoint.iter('{http://www.opengis.net/gmlcov/1.0}positions'):
                                timestamps = positions.text
                                ts2 = timestamps.split('\n')
                    for rangeSet in MultiPointCoverage.iter('{http://www.opengis.net/gml/3.2}rangeSet'):
                        for DataBlock in rangeSet.iter('{http://www.opengis.net/gml/3.2}DataBlock'):
                            for doubleOrNilReasonTupleList in DataBlock.iter('{http://www.opengis.net/gml/3.2}doubleOrNilReasonTupleList'):
                                measurements = doubleOrNilReasonTupleList.text
                                me2 = measurements.split('\n')
    ts2 = [x for x in ts2 if x != '']
    me2 = [x for x in me2 if x != '']
    observations = []
    for i in range (len(me2)-1):
        observation = []
        ts3 = ts2[i].split(' ')
        unixtime = int(ts3[len(ts3)-1])
        utc_time = dt.datetime.fromtimestamp(unixtime)
        local_time = utc_time.strftime("%Y-%m-%d %H:%M")
        observation.append(local_time)
        me3 = me2[i].split(' ')
        me3 = [x for x in me3 if x != '']
        for j in range (len(me3)):
            observation.append(float(me3[j]))
        observations.append(observation)

    for t in range (len(observations)):
        x1.append(observations[t][0])
        y1.append(observations[t][1])

    weather_baga_url = "http://opendata.fmi.fi/wfs?request=getFeature&storedquery_id=fmi::observations::weather::multipointcoverage&fmisid=100969&parameters=Temperature,Humidity,DewPoint,WindSpeedMS,WindDirection,WindGust"
    data = requests.get(weather_baga_url)
    root = ET.fromstring(data.text)
    for member in root.iter('{http://www.opengis.net/wfs/2.0}member'):
        for GridSeriesObservation in member.iter('{http://inspire.ec.europa.eu/schemas/omso/3.0}GridSeriesObservation'):
            for result in GridSeriesObservation.iter('{http://www.opengis.net/om/2.0}result'):
                for MultiPointCoverage in result.iter('{http://www.opengis.net/gmlcov/1.0}MultiPointCoverage'):
                    for domainSet in MultiPointCoverage.iter('{http://www.opengis.net/gml/3.2}domainSet'):
                        for SimpleMultiPoint in domainSet.iter('{http://www.opengis.net/gmlcov/1.0}SimpleMultiPoint'):
                            for positions in SimpleMultiPoint.iter('{http://www.opengis.net/gmlcov/1.0}positions'):
                                timestamps = positions.text
                                ts2 = timestamps.split('\n')
                    for rangeSet in MultiPointCoverage.iter('{http://www.opengis.net/gml/3.2}rangeSet'):
                        for DataBlock in rangeSet.iter('{http://www.opengis.net/gml/3.2}DataBlock'):
                            for doubleOrNilReasonTupleList in DataBlock.iter('{http://www.opengis.net/gml/3.2}doubleOrNilReasonTupleList'):
                                measurements = doubleOrNilReasonTupleList.text
                                me2 = measurements.split('\n')
    ts2 = [x for x in ts2 if x != '']
    me2 = [x for x in me2 if x != '']
    observations2 = []
    for i in range (len(me2)-1):
        observation = []
        ts3 = ts2[i].split(' ')
        unixtime = int(ts3[len(ts3)-1])
        utc_time = dt.datetime.fromtimestamp(unixtime)
        local_time = utc_time.strftime("%Y-%m-%d %H:%M")
        observation.append(local_time)
        me3 = me2[i].split(' ')
        me3 = [x for x in me3 if x != '']
        for j in range (len(me3)):
            observation.append(float(me3[j]))
        observations2.append(observation)

    for t in range (len(observations2)):
        x2.append(observations2[t][0])
        y2.append(observations2[t][1])
    
    miny = min(min(y1),min(y2))
    maxy = max(max(y1),max(y2))
    ran = max(maxy-miny,10)
    minv = int(int(miny/5.0)*5.0)-5
    maxv = int(int(maxy/5.0)*5.0)+5


    return render_template('line_chart.html', title='Inkoo-temp', xa=x1, ya=y1, xb=x2, yb=y2, sy=maxv, py=minv)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)