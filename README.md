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

- `/category` (LOM-DE + extension)
- `/conditionsOfAccess` (custom vocab, inspired by <schema.org/conditionsOfAccess>)
- `/containsAvertisement` (custom vocab)
- `/discipline` (LOM-DE)
- `/educationalContext` (LOM-DE)
- `/intendedEndUserRole` (LOM-DE)
- `/interface` (custom vocab)
- `/learningResourceType` (LOM-DE)
- `/lifecycleContributeRole` (LOM-DE)
- `/rightsCopyrightAndOtherRestrictions` (LOM-DE)
- `/rightsCost` (LOM-DE, added a category "yes_for_additional", which indicates that additional content/features are purchasable)
- `/sourceContentType` (custom vocab)
- `/toolCategory` (custom vocab)
- `/educationalRole` ([LRMI](https://www.dublincore.org/specifications/lrmi/concept_schemes))
- `/alignmentType` ([LRMI](https://www.dublincore.org/specifications/lrmi/concept_schemes))
- `/educationalUse` ([LRMI](https://www.dublincore.org/specifications/lrmi/concept_schemes))
- `/interactivityType` ([LRMI](https://www.dublincore.org/specifications/lrmi/concept_schemes))

## /vocab_string/<string:name>

Same as above, but only outputs id and preferred german label. Sooner or
later this will be merged with above endpoint and handled via query parameters.

## API documentation for OpenSalt

- [Documentation](https://opensalt.net/api/doc/#/)

## Links

- [OpenEduHub metadata scheme](https://sroertgen.github.io/oer-metadata-hub-scheme/draft_version/index.html)
- [LOMv1.0](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1032843)
- [LOMv1.0](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1532505)
- [LOM-DE](http://sodis.de/lom-de/LOM-DE.doc)
- [LOM-EAF](https://sodis.de/lom-eaf/LOM-EAF_v0.3.pdf)
- [HS-LOM](https://dini-ag-kim.github.io/hs-oer-lom-profil/latest/)
- [LRMI](https://www.dublincore.org/specifications/lrmi/)
- [LOM-CH](https://www.educa.ch/sites/default/files/uploads/2018/05/lom-chv2.0_de.pdf)