# OER-Flask-Api

This container will build up a flask app to handle REST-API calls.
Its purpose is mainly to get SKOS vocabulary and parse competence frameworks.
It is closley developed to serve:
  - [OER-Metadata-Editor](https://github.com/sroertgen/oer-metadata-editor)

## Requirements

- Make a virtual environemnt: `python -m venv oerhoernchen`
- activate it: `source oerhoernchen/bin/activate`
- Install requirements with `pip install -r requirements.txt`

## How to use

- run app locally with: `python app.py`

## Endpoints

### /frameworks

This endpoint calls an [OpenSalt](https://www.opensalt.net/about)-Instance at <http://c108-059.cloud.gwdg.de:3000/>.



## API calls for OpenSalt

- [Documentation](https://opensalt.net/api/doc/#/)
