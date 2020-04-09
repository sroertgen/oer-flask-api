# OER-Flask-Api

This container will build up a flask app to handle REST-API calls.
Its purpose is mainly to get SKOS vocabulary and parse competence frameworks.
It is closley developed to serve:

- [OER-Metadata-Editor](https://github.com/sroertgen/oer-metadata-editor)

## Requirements

- Make a virtual environemnt: `python -m venv oer-flask-api`
- activate it: `source oer-flask-api/bin/activate`
- Install requirements with `pip install -r requirements.txt`

## How to use

The API listens on port 5000.

### Run local

- run app locally with: `python app.py`

### Run with docker

This repo is connected to DockerHub and gets build automatically. You can use the latest version as a docker container with:

- `docker pull laocoon667/oer-flask-api:latest`

Then run with:

- `docker run --rm -d  -p 5000:5000/tcp laocoon667/oer-flask-api:latest`

## Endpoints

### /frameworks

This endpoint calls an [OpenSalt](https://www.opensalt.net/about)-Instance at <http://c108-059.cloud.gwdg.de:3000/>.

It returns a JSON in tree strucutre. It providesthe following informations:

- `id`: returns the id of the document or item in OpenSalt. If it is the root node, it is equal to `label`
- `label`: the label of the document or item
- `children`: contains a list of child items
- `educationalFramework`: the educational Framework the item belongs to
- `creator`: the creator of the educational Framework
- `language`: lanuage of the item
- `educationalLevel`: represents th educational level of respective item
- `fullStatement`: a description of the item
- `associationType`: describes association to another item
  - `destinationNodeURI`: provides `title`, `identifier` and `uri` of the associated item

### /vocab/<string:name>

This endpooint can be used to get defined vocabulary.

Its outputs are:

- `id`: points to the definition of the vocab
- `label`: is an array which contains a language property and the respective value in the defined vocabulary
- `description`: is an array which contains a language property and the respective description of the defined vocabulary
- `altId`: is an array which contains a language property and the respective alternative labels of the defined vocabulary

Current implemented vocabs are:

- `/alignmentType` (LRMI)
- `/category` (LOM-DE + extension)
- `/discipline` (LOM-DE)
- `educationalContext` (LOM-DE)
- `/educationalRole` (LRMI)
- `/educationalUse`(LRMI)
- `/intendedEndUserRole` (LOM-DE)
- `/interactivityType` (LRMI)
- `/learningResourceType` (LOM-DE)
- `/lifecycleContributeRole` (LOM-DE)
- `/rightsCopyrightAndOtherRestrictions` (LOM-DE)
- `/rightsCost` (LOM-DE)
- `/sourceContentType` (custom vocab)

## API documentation for OpenSalt

- [Documentation](https://opensalt.net/api/doc/#/)

## Reference

- TODO