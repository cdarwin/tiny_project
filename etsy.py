#!/usr/bin/env python

# Import the web.py library to make writing web applications easier
# http://webpy.org/
import web

# Initialise a database object using MySQL credentials
# http://webpy.org/docs/0.3/tutorial#databasing
db = web.database(
        dbn='mysql',
        user='dbuser',
        pw='dbpass',
        db='dbname'
)

# Initialise a render object for simple HTML templates
# http://webpy.org/docs/0.3/tutorial#templating
render = web.template.render('templates/')


# Initialise URL structure (routes)
# http://webpy.org/docs/0.3/tutorial#urlhandling
urls = (
    '/', 'Index',
    '/add', 'Add',
    '/list', 'List'
)

class Index:
    """Index handler for / route

    This is a simple example class that does very little

    """

    def GET(self):
        """Simple method for GETs to the / route"""
        return "Hello, world!"

class List:
    """List handler for /list route"""

    def GET(self):
        """ SELECT * FROM items """
        items = db.select('items')
        return render.index(items)

class Add:
    """Add handler for /add route"""

    """Here we define a form to simplify building our HTML laster"""
    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, 
            size=30,
            description="Item name:"),
        web.form.Textbox('price', web.form.notnull, 
            size=30,
            description="Item price:"),
        web.form.Textarea('descrip', web.form.notnull, 
            rows=30, cols=80,
            description="Item description:"),
        web.form.Button('Post entry'),
    )

    def GET(self):
        """Print the form for user input"""
        form = self.form()
        return render.add(form)

    def POST(self):
        form = self.form()
        """Make sure the contents of the form are valid"""
        if not form.validates():
            return render.add(form)
        """Insert the elements of the form into the database"""
        db.insert(
                'items',
                title=form.d.title,
                descrip=form.d.descrip,
                price=form.d.price
        )
        """Redirect users to the /list page for immediate 
        feedback that the insert was succesful"""
        raise web.seeother('/list')

# Necessary boilerplate
app = web.application(urls, globals())
# Necessary line for CGI nuances
web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)

# More necessary boilerplate
if __name__ == "__main__":
        app.run()
