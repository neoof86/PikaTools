from flask import Flask, request, render_template, redirect#, send_file
import subprocess
import datetime
import json
import csv

app = Flask(__name__)
racename = ""
checkpointname = ""

def readjson(racename, checkpointname):
    racedata = []
    try:
        f = open('data.json')
        data = json.load(f)
        for record in data:
            if record['race'] == racename and record['checkpoint'] == checkpointname:
                racedata = record['data']
        f.close()
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        racedata = []
    return racedata

def updatejson(racename, checkpointname, racedata):
    updated = False
    try:
        f = open('data.json')
        data = json.load(f)
        for record in data:
            if record['race'] == racename and record['checkpoint'] == checkpointname:
                record['data'] = racedata
                updated = True
        if not updated:
            newracedata = {
                "race": racename,
                "checkpoint": checkpointname,
                "data": racedata
            }
            data.append(newracedata)
        f.close()
        f = open('data.json', 'w')
        f.write(json.dumps(data))
        f.close()
    except (FileNotFoundError):
        f = open('data.json', 'x')
        f = open('data.json', 'w')
        newracedata = {
            "race": racename,
            "checkpoint": checkpointname,
            "data": racedata
        }
        data = []
        data.append(newracedata)
        f.write(json.dumps(data))
        f.close()
    return racedata

def csvexport(rname, cname):
    f = open('data.json')
    data = json.load(f)
    for record in data:
        if record['race'] == rname and record['checkpoint'] == cname:
            racedata = record['data']
    filename = f"/racefiles/{rname}-cp-{cname}-{datetime.date.today().year}.csv"
    with open(filename, mode='w') as resultscsv:
        resultscsvwriter = csv.writer(resultscsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        resultscsvwriter.writerow(['ColA', 'ColB', 'ColC', 'BibTime', 'Bib'])
        resultscsvwriter.writerow(['', '', '', '', ''])
        for record in racedata:
            resultscsvwriter.writerow(['', '', '', record['ts'], record['bib']])
    f.close()
    
@app.route('/')
def recordrace():
    return render_template('race.html')

@app.route('/', methods=['POST'])
def race_post():
    global racename
    global checkpointname
    racename = request.form['race']
    checkpointname = request.form['checkpoint']
    return redirect("/checkpoint")

@app.route('/checkpoint')
def checkpoint():
    data = readjson(racename, checkpointname)
    return render_template("checkpoint.html", data=data, race=racename, checkpoint=checkpointname)

@app.route('/checkpoint', methods=['POST'])
def checkpoint_post():
    data = readjson(racename, checkpointname)
    runnerid = request.form['runnerid']
    runner = {
        "bib": runnerid,
        "ts": str(datetime.datetime.now().strftime("%H%M%S%f"))[:-4]
    }
    data.append(runner)
    updatejson(racename, checkpointname, data)
    csvexport(racename, checkpointname)
    return render_template("checkpoint.html", data=data, race=racename, checkpoint=checkpointname)

#@app.route('/csv')
#def csvpage():
#    return render_template("csv.html")
#
#@app.route('/csv', methods=['POST'])
#def csv_post():
#    rname = request.form['race']
#    cname = request.form['checkpoint']
#    csvexport(rname, cname)
#    return send_file('raceresults.csv', as_attachment=True)

@app.route("/reboot")
def reboot():
    subprocess.run("sudo shutdown -r now".split())
    return "Restarting the OS"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)