from flask_restful import Resource, reqparse
import json
import rdflib

# Use the parse functions to point directly at the URI

uris = {
    'alignmentType': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/alignmentType.ttl',
    'category': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/category.ttl',
    'discipline': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/discipline.ttl',
    'educationalRole': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/educationalAudienceRole.ttl',
    'educationalContext': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/educationalContext.ttl',
    'educationalUse': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/educationalUse.ttl',
    'intendedEndUserRole': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/intendedEndUserRole.ttl',
    'interactivityType': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/interactivityType.ttl',
    'learningResourceType': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/learningResourceType.ttl',
    'lifecycleContributeRole': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/lifecycleContributeRole.ttl',
    'rightsCopyrightAndOtherRestrictions': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/rightsCopyrightAndOtherRestrictions.ttl',
    'rightsCost': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/rightsCost.ttl',
    'sourceContentType': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/sourceContentType.ttl'
}


class VocabString(Resource):
  @classmethod
  def get_vocab_string(cls, name):
    label_list = []
  # initialize Graph
    graph = rdflib.Graph()
    g = graph.parse(uris.get(name), format="n3")
    g_serialized = g.serialize(format='json-ld', indent=4)
    y = json.loads(g_serialized)

    for item in y:
        try:
            label_de = next(
                (item['@value'] for item in item['http://www.w3.org/2004/02/skos/core#prefLabel'] if item['@language'] == "de"), None)
            string = item['@id'].split('/')[-1] + ' : ' + label_de
            label_list.append(string)
        except:
            pass
    print(label_list)
    return label_list

  def get(self, name):
    vocab_string = self.get_vocab_string(name)
    return { 
      'vocabs': vocab_string
      }

