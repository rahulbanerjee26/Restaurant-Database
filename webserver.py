from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import queries_restaurant
import queries_menu


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body> <h1> Restaurants in database</h1>"
                output+= "<h2><a href=/restaurants/new> Create New Restaurant</a></h2>"
                restaurants = queries_restaurant.list_all()
                for restaurant in restaurants:
                    output += "<h3> %s</h3> <a href='restautrants/%s/menu'> View Menu </a><br> <a href='restautrants/%s/delete'>Delete</a> <br> <a href='/restautrants/%s/edit'>Edit</a>" %(restaurant.name,restaurant.id,restaurant.id,restaurant.id)
                output+="</body></html>"
                self.wfile.write(output)
                print (output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return   

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                id = self.path.split("/")[2]
                restaurant = queries_restaurant.find_restaurant(id)
                output = "<html><body>"
                output+= "<h1>Edit %s</h1>" %restaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurant.id
                output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % restaurant.name
                output += "<input type = 'submit' value = 'Rename'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                id = self.path.split("/")[2]
                restaurant = queries_restaurant.find_restaurant(id)
                output = ""
                output += "<html><body>"
                output += "<h1>Delete Restaurant</h1>"
                output += "<h2> Are you sure you want to delete the restaurant %s </h2>" %restaurant.name
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/delete'>" %restaurant.id
                output += "<input type='submit' value='Delete'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return  

            if self.path.endswith("/menu"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                id = self.path.split("/")[2]
                menu = queries_menu.show_menu(id)
                restaurant = queries_restaurant.find_restaurant(id)
                output = ""
                output += "<html><body>"
                output += "<h1>Menu of %s</h1>" %restaurant.name
                output += "<h2> <a href='menu/add'> Add Item </a> </h2>"
                output += "<h2> <a href='/restaurants'> Go Back </a> </h2>"
                for menu_item in menu:
                    output += " <h3> %s </h3>" %(menu_item.name)
                    output += " <h6> %s </h6>" %(menu_item.course)
                    output+= "<p> %s </p>" %(menu_item.description)
                    output += "<h4> <i> %s <br> <br></i>" %(menu_item.price) 
                output += "</form></body></html>"
                self.wfile.write(output)
                return   

            if self.path.endswith("/menu/add"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                id = self.path.split("/")[2]
                restaurant = queries_restaurant.find_restaurant(id)
                output = ""
                output += "<html><body>"
                output += "<h1> Add item to menu of %s </h1>" %restaurant.name
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/menu/add'>" %restaurant.id
                output += "<input type='text' name='item_name' placeholder='name'> <br>"
                output += "<input type='text' name='item_entree' placeholder='entree'> <br> "
                output += "<input type='text' name='item_des' placeholder='description'> <br>"
                output += "<input type='text' name='item_price' placeholder='price'>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/menu/add'>" %restaurant.id
                output += "<input type='submit' value='Add Menu Item'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return 


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
                
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                #extract the name
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('newRestaurantName')
                    queries_restaurant.add_restaurant(name[0])
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                #extract the name
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
                id = self.path.split("/")[2]
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('newRestaurantName')
                    queries_restaurant.edit_restaurant(id,name[0])
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

            if self.path.endswith("/delete"):
                id = self.path.split("/")[2]
                queries_restaurant.delete_restaurant(id)
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()

            if self.path.endswith("/menu/add"):
                id = self.path.split("/")[2]
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    it_name = fields.get('item_name')
                    it_des   = fields.get('item_des')
                    it_price = fields.get('item_price')
                    it_entree = fields.get('item_entree')
                    queries_menu.add_item(id,it_name[0],it_des[0],it_entree[0],it_price[0])
                self.send_response(301)
                self.send_header('content-type','text/html')
                self.send_header('Location','/restaurants/%s/menu' %id) 
                self.end_headers()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print ("Web Server running on port %s") % port
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()






