from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import os

if 'PHOTODB_PORT' not in os.environ:
    raise Exception("Required PHOTODB_PORT environment variable is not set")
if 'PHOTODB_DB_NAME' not in os.environ:
    raise Exception("Required PHOTODB_DB_NAME environment variable is not set")


import tinyurl

db_connect = create_engine('sqlite:///data/{}'.format(os.environ['PHOTODB_DB_NAME']))
conn = db_connect.connect() # connect to database
app = Flask(__name__, static_folder='static')
api = Api(app)

#RESTFUL API
class PhotoDB(Resource):
    def get(self, collection_name, primary):
        query = conn.execute("select * from {0} where photo_primary = {1}".format(collection_name, primary) )
        #print(query.cursor.fetchall())
        return {'photos': [ (i[1],i[2],i[3]) for i in query.cursor.fetchall()]}
    
    def post(self,collection_name, primary):
        
        if collection_name == "create":   #CREATE TABLE
            print("Creating New Table Entry....{0}".format(primary))
            query = conn.execute("create table {0} ( photo_id integer PRIMARY KEY, photo_name text NOT NULL, photo_link text NOT NULL, photo_tiny_link text NOT NULL, photo_primary bool NOT NULL)".format(primary))
            return
        elif collection_name == "delete": #DELETE TABLE, not for normal use.
            print("Deleting Table Entry....{0}".format(primary))
            query = conn.execute("drop table {0}".format(primary))
            return
        else:                             #INSERT ENTRY TO TABLE
            photo_name = request.json['photo_name']
            if "thumb" in photo_name: #if thumb in picture dont register it
                return { 'slink': 0 }
            photo_link = request.json['photo_link']
            photo_tiny_link = tinyurl.create_one(str(photo_link))
            photo_primary = int(primary)
        
            query = conn.execute("insert into {0} values(null,'{1}','{2}','{3}',{4})".format(
                                 collection_name,photo_name, 
                                 photo_link, photo_tiny_link, photo_primary))
            return {'slink': photo_tiny_link}

api.add_resource(PhotoDB, '/rest/<collection_name>/<primary>')

def queryDictList( queryStr ):
    query = conn.execute(queryStr)
    return [ dict(zip(query.keys(), i)) for i in query.cursor.fetchall() ]

#GALLERY PAGE
@app.route('/gallery/<collection>')
@app.route('/gallery/<collection>/')
@app.route('/gallery/<collection>/<pic>')
def photodb_gallery(collection, pic=None):

    tImages = { t['grp'] : t for t in queryDictList(f"select * from {collection} where thumb = 1") }
    pImages = { p['grp'] : p for p in queryDictList(f"select * from {collection} where photo_primary = 1") }
    # Multiple Secondary Images need appending
    sImages = {}
    for s in  queryDictList(f"select * from {collection} where photo_primary = 0 and thumb = 0"):
        sImages[s['grp']] = sImages.get(s['grp'],[]) + [s]

    images = {}
    for t in tImages.keys():
        images[t] = { 'thumb':None, 'primary':None, 'secondary':[] }
        images[t]['thumb']     = tImages.get(t, None)
        images[t]['primary']   = pImages.get(t, None)
        images[t]['secondary'] = sImages.get(t, None)

    event_name = collection.replace("_", " ").title() 
    return render_template('index.html', event_name=event_name, images=images, pic=pic)

@app.route('/gallery/fonts/<filename>')  
def send_font(filename):  
    return send_from_directory('static/fonts', filename)

@app.route('/gallery/css/<filename>')  
def send_css(filename):  
    return send_from_directory('static/css', filename)

if __name__ == '__main__':
     app.run( port=os.environ['PHOTODB_PORT'] )
