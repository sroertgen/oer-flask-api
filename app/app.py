from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from vocabs import Vocab
from vocabs_string import VocabString
from frameworks import Frameworks
from frameworks_ld import Frameworks_ld


# config
app = Flask(__name__)
app.secret_key = 'changethisinproduction'
api = Api(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Database

# Add Classes to API
api.add_resource(Vocab,
                 '/vocab/<string:name>',
                 '/vocabs/<string:name>')
api.add_resource(VocabString, '/vocab_string/<string:name>')
api.add_resource(Frameworks, '/frameworks')
api.add_resource(Frameworks_ld,
                 '/frameworks_ld',
                 '/frameworks_ld/<string:framework>')

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
