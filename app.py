from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from vocabs import Vocab
from frameworks import Frameworks

# config
app = Flask(__name__)
app.secret_key = 'changethisinproduction'
api = Api(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Database

# Add Classes to API
api.add_resource(Vocab, '/vocab/<string:name>')
api.add_resource(Frameworks, '/frameworks')

# Run app
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
