from sqlalchemy import create_engine
import tinyurl

db_connect = create_engine('sqlite:///photo.db')

#Create Db Table
conn = db_connect.connect() # connect to database

collection_name= "george_fiona_wedding_2018"
#query = conn.execute("create table {0} ( photo_id integer PRIMARY KEY, photo_name text NOT NULL, photo_link text NOT NULL, photo_tiny_link text NOT NULL, photo_primary bool NOT NULL)".format(collection_name))

for num in range(1,51):
   #Main Photo
   photo_name = "pic"+str(num).zfill(5)+".jpg"
   photo_link = "https://filedn.com/lON9Nk3nzUs4KheBfvjzRuF/photobooth/{0}/{1}".format(collection_name, photo_name)
   cmd = "insert into {0} values(null,'{1}','{2}','{3}',{4})".format( collection_name,photo_name, photo_link, tinyurl.create_one(str(photo_link)), 1)
   print cmd
   query = conn.execute(cmd)

   #Seperate Components of main
   for comp in range(4):
       photo_name = "pic"+str(num).zfill(5)+"."+str(comp)+".jpg"
       photo_link = "https://filedn.com/lON9Nk3nzUs4KheBfvjzRuF/photobooth/{0}/{1}".format(collection_name, photo_name)
       cmd = "insert into {0} values(null,'{1}','{2}','{3}',{4})".format( collection_name,photo_name, photo_link, tinyurl.create_one(str(photo_link)), 0)
       print cmd
       query = conn.execute(cmd)
