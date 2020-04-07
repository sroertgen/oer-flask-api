from flask_restful import Resource, reqparse
import requests

base_url = 'http://141.5.108.59:3000/ims/case/v1p0'

r = requests.get(base_url + '/CFDocuments')

list_of_documents = []

for item in r.json()['CFDocuments']:
   list_of_documents.append(item['identifier'])

print(f'List of Documents is: {list_of_documents}')

class Frameworks(Resource):
  @classmethod
  def get_all(cls):
    competence_frameworks = []

    for item in list_of_documents:
      print(f'current item: {item}')
      r = requests.get(base_url + '/CFPackages/' + item)

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
        str_title = r.json()['creator']
        print(str_title)
        competence_framework.append(('Root', node))
        competence_framework.append(('Title', r.json()['creator']))

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
                d['id'] = str_title
                d['label'] = str_title
              else:
                d['id'] = r.json()['identifier']
                d['label'] = r.json()['title']
                d['educationalFramework'] = r.json()['title']
                d['creator'] = r.json()['creator']
                d['language'] = r.json()['language']
          else:
            # this is a items URI
            d['id'] = r.json()['identifier']
            d['label'] = r.json()['humanCodingScheme']
            d['educationalFramework'] = r.json()['CFDocumentURI']['title']
            d['educationLevel'] = r.json()['educationLevel']
            d['fullStatement'] = r.json()['fullStatement']

          for item in associations:
                if item['originNodeURI']['identifier'] == d['id']:
                    d['associationType'] = item['associationType']
                    d['destinationNodeURI'] = item['destinationNodeURI']

        except:
          pass
        children = get_children(node)
        if children:
            d['children'] = [get_nodes(child) for child in children]
        return d

      def get_children(node):
          return [x[1] for x in competence_framework if x[0] == node]

      tree = get_nodes('Root')
      # competence_frameworks.append(tree['children'][0])
      competence_frameworks.append(tree)
  
    return competence_frameworks

  def get(self):
    competence_frameworks = self.get_all()

    return {'frameworks': competence_frameworks}
