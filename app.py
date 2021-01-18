# import necessary libraries
#from models import create_classes
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask_sqlalchemy import SQLAlchemy
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "postgresql://postgres:postgres@localhost:5432/demo_db_1"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connects to the database using the app config
db = SQLAlchemy(app)


# create engine so we can use automap_base
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Appartments = Base.classes.appartments

#################################################
# Endpoints Setup
#################################################
# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

#endpoint that displays a portion of the data
@app.route("/data")
def data ():
    results = db.session.query(Appartments.rent, Appartments.bedrooms, Appartments.bathrooms, Appartments.size_sqft)
    appartment_data = []
    for result in results:
        appartment_data.append({
            "rent":result[0],
            "bedrooms":result[1],
            "bathroom":result[2],
            "size_sqft":result[3]
        })
    return jsonify(appartment_data)


if __name__ == "__main__":
    app.run()