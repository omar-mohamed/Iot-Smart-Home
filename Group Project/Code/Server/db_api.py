from flask import Flask, render_template
import sqliteDB, json

DB_PATH = "Board_Location.db"

app = Flask(__name__)


##@app.route('/map')
##def display_map():
##    return render_template('map.html')

@app.route('/get_loc')
def get_loc():
    return json.dumps(sqliteDB.getMostRecentData(DB_PATH))


app.run(debug=True)
