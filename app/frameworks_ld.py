from flask_restful import Resource, reqparse
import requests
import json

base_url = 'http://141.5.108.59:3000/ims/case/v1p0'

r = requests.get(base_url + '/CFDocuments')

list_of_documents = []

for item in r.json()['CFDocuments']:
    document = {}
    document['title'] = item['title']
    document['identifier'] = item['identifier']
    list_of_documents.append(document)

print(f'List of Documents is: {list_of_documents}')

with open('context.json', 'r') as f:
  context = json.load(f)

class Frameworks_ld(Resource):
  @classmethod
  def get_all_frameworks(cls):
    competence_frameworks = []
    print(list_of_documents)
    for item in list_of_documents:
      print(f'current item: {item}')
      r = requests.get(base_url + '/CFPackages/' + item['identifier'])

      competence_framework = []
      associations = []

      for item in r.json()['CFAssociations']:
        if item['associationType'] == 'isChildOf':
          competence_framework.append(
            (item['destinationNodeURI']['identifier'],
            (item['originNodeURI']['identifier']))
            )
        else:
          association = {
                'associationType': item['associationType'],
                'originNodeURI': item['originNodeURI'],
                'destinationNodeURI': item['destinationNodeURI']
            }
          associations.append(association)

      parents, children = zip(*competence_framework)
      root_nodes = {x for x in parents if x not in children}
      for node in root_nodes:
        r = requests.get('http://141.5.108.59:3000/ims/case/v1p0/CFDocuments/' + node)
        concept_scheme_title = {r.json()['language']: r.json()['title']}
        concept_scheme_creator = {r.json()['language']: r.json()['creator']}
        concept_scheme_id = r.json()['uri']

        competence_framework.append(('Root', node))
        competence_framework.append(('Title', r.json()['title']))

      def get_nodes(node):
        d = {}
        try:
          d['id'] = node
          r = requests.get(
              base_url + '/CFItems/' + d['id'])

          if r.status_code == 404:
              # this might be a package URI
              r = requests.get(
                  base_url + '/CFDocuments/' + d['id'])
              if node == "Root":
                pass
              else:
                d['id'] = concept_scheme_id
                d['type'] = "ConceptScheme"
                d['title'] = concept_scheme_title
                d['creator'] = concept_scheme_creator
                d['@context'] = context
                # d['id'] = r.json()['uri']
                # d['type'] = "Concept"
                # d['prefLabel'] = {r.json()['language']: r.json()['humanCodingScheme']}
                # d['educationalFramework'] = r.json()['title']
                # d['creator'] = r.json()['creator']
                # d['language'] = r.json()['language']
                # d['inScheme'] = concept_scheme_id
          else:
            # this is a items URI
            d['id'] = r.json()['uri']
            d['type'] = "Concept"
            d['prefLabel'] = {r.json()['language']: r.json()['humanCodingScheme']}
            # d['educationalFramework'] = r.json()['CFDocumentURI']['title']
            # d['educationLevel'] = r.json()['educationLevel']
            d['definition'] = {r.json()['language']: r.json()['fullStatement']}
            # d['inScheme'] = concept_scheme_id.split("/")[-1]

          # for item in associations:
          #       if item['originNodeURI']['identifier'] == d['id']:
          #           d['associationType'] = item['associationType']
          #           d['destinationNodeURI'] = item['destinationNodeURI']

        except:
          pass
        children = get_children(node)
        if children:
            d['narrower'] = [get_nodes(child) for child in children]
        return d

      def get_children(node):
          return [x[1] for x in competence_framework if x[0] == node]

      tree = get_nodes('Root')
      competence_frameworks.append(tree['narrower'])

    return competence_frameworks

  @classmethod
  def get_framework(cls, framework):
    competence_frameworks = []
    r = requests.get(base_url + '/CFPackages/' + framework)

    competence_framework = []
    associations = []

    for item in r.json()['CFAssociations']:
      if item['associationType'] == 'isChildOf':
        competence_framework.append(
          (item['destinationNodeURI']['identifier'],
          (item['originNodeURI']['identifier']))
          )
      else:
        association = {
              'associationType': item['associationType'],
              'originNodeURI': item['originNodeURI'],
              'destinationNodeURI': item['destinationNodeURI']
          }
        associations.append(association)

    parents, children = zip(*competence_framework)
    root_nodes = {x for x in parents if x not in children}
    print(root_nodes)
    node = framework
    # for node in root_nodes:
    #   print(f"Root nodes: {root_nodes}")
    #   print(f"node: {node}")
    r = requests.get('http://141.5.108.59:3000/ims/case/v1p0/CFDocuments/' + node)
    concept_scheme_title = {r.json()['language']: r.json()['title']}
    concept_scheme_creator = {r.json()['language']: r.json()['creator']}
    concept_scheme_id = r.json()['uri']

    competence_framework.append(('Root', node))
    competence_framework.append(('Title', r.json()['title']))

    def get_nodes(node):
      d = {}
      try:
        d['id'] = node
        r = requests.get(
            base_url + '/CFItems/' + d['id'])

        if r.status_code == 404:
            # this might be a package URI
            r = requests.get(
                base_url + '/CFDocuments/' + d['id'])
            if node == "Root":
              pass
            else:
              d['id'] = concept_scheme_id
              d['type'] = "ConceptScheme"
              d['title'] = concept_scheme_title
              d['creator'] = concept_scheme_creator
              d['@context'] = context
              # d['id'] = r.json()['uri']
              # d['type'] = "Concept"
              # d['prefLabel'] = {r.json()['language']: r.json()['humanCodingScheme']}
              # d['educationalFramework'] = r.json()['title']
              # d['creator'] = r.json()['creator']
              # d['language'] = r.json()['language']
              # d['inScheme'] = concept_scheme_id
        else:
          # this is a items URI
          d['id'] = r.json()['uri']
          d['type'] = "Concept"
          d['prefLabel'] = {r.json()['language']: r.json()['humanCodingScheme']}
          # d['educationalFramework'] = r.json()['CFDocumentURI']['title']
          # d['educationLevel'] = r.json()['educationLevel']
          d['definition'] = {r.json()['language']: r.json()['fullStatement']}
          # d['inScheme'] = concept_scheme_id.split("/")[-1]

        # for item in associations:
        #       if item['originNodeURI']['identifier'] == d['id']:
        #           d['associationType'] = item['associationType']
        #           d['destinationNodeURI'] = item['destinationNodeURI']

      except:
        pass
      children = get_children(node)
      if children:
          d['narrower'] = [get_nodes(child) for child in children]
      return d

    def get_children(node):
        return [x[1] for x in competence_framework if x[0] == node]

    tree = get_nodes('Root')
    competence_frameworks.append(tree['narrower'][0])

    return competence_frameworks[0]

  def get(self, framework=''):
    print(framework)
    if framework == "all":
      response = self.get_all_frameworks()
    elif framework == '' or 'list_of_documents':
      response = list_of_documents
    else:
        for item in list_of_documents:
            if framework == item['identifier']:
              response = self.get_framework(framework)
              break
            else:
              response = ("Did not find matching document"), 404

    return response, 200
