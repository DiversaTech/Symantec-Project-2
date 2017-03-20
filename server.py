from flask import Flask
app = Flask('Email Extraction')

# Home Page
@app.route('/')
def index():
    return 'Sample text'

# To add routes, just use @app.route(path)
# Solid documentation is on flask.pocoo.org
# Flask is extremely modular, so you might be able to use the Google Python API
# If you need to add specific packages/modules, make sure to add to the requirements.txt file

if __name__ == '__main__':
    app.run()