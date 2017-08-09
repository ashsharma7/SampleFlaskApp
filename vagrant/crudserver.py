from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine) 
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "&#161Hola \n<a href = '/hello'>Back to Hello</a>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith(("/restaurants", "/restaurants/", "/restaurants/list", "/restaurants/list/")):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = self.listRestaurants()
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/edit"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = self.listRestaurants(True)
                self.wfile.write(output)
                print output
                return

            if "/restaurant/edit/" in self.path:
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                
                output = ""
                output += "<html><body>"
                output += "Enter new name of the restaurant in the box below<br>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/rename'><h2>Enter new name of restaurant</h2><input name="newNameRestaurant" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith(("/restaurants/new", "/restaurants/new/")):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "Enter name of new restaurant in the box below<br>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Enter name of new restaurant</h2><input name="newRestaurantName" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404,"File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith(("/restaurants/new", "/restaurants/new/")):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                #pdict['boundary'] = pdict['boundary'].encode('utf-8')
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print "fields = ", fields
                    messagecontent = fields.get('newRestaurantName')
                    newRestaurantName = messagecontent[0]
                    if len(newRestaurantName) > 0:
                        print "adding new restr"
                        self.addRestaurant(newRestaurantName)
                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

            if self.path.endswith(("/restaurant/rename", "/restaurant/rename/")):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                #pdict['boundary'] = pdict['boundary'].encode('utf-8')
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print "fields = ", fields
                    messagecontent = fields.get('newRestaurantName')
                    newRestaurantName = messagecontent[0]
                    if len(newRestaurantName) > 0:
                        print "adding new restr"
                        self.addRestaurant(newRestaurantName)
                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

            if self.path.endswith(("/restaurants/delete", "/restaurants/delete/")):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                #pdict['boundary'] = pdict['boundary'].encode('utf-8')
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print "fields = ", fields
                    messagecontent = fields.get('newRestaurantName')
                    newRestaurantName = messagecontent[0]
                    if len(newRestaurantName) > 0:
                        print "adding new restr"
                        self.addRestaurant(newRestaurantName)
                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()
            '''
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''
            '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            '''output += "</body></html>"
            self.wfile.write(output)
            print output'''

        except:
            pass

    def listRestaurants(self,editable=False):
        output = ""
        output += "<html><body>"
        restaurants = session.query(Restaurant).all()
        for r in restaurants:
            output += r.name + '<br>'
            if editable:
                output += "<a href = '/restaurant/edit/%s'>Edit</a><br>" % r.id
                output += "<a href = '/restaurant/delete/%s'>Delete</a><br>" % r.id
        if editable:
            output += "<br><a href = '/restaurants/new'>Add a New Restaurant</a><br>"
        output += "</body></html>"
        return output

    def addRestaurant(self, rName):
        newR = Restaurant(name = rName)
        session.add(newR)
        session.commit()

    def deleteRestaurant(self, rName):
        restrToDelete = session.query(Restaurant).filter_by(name = rName).one()
        session.delete(restrToDelete)
        session.commit()

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered. Stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()
