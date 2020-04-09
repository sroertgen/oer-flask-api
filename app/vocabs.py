from flask_restful import Resource, reqparse
import json
import rdflib

# Use the parse functions to point directly at the URI

uris = {
    'alignmentType': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/alignmentType.ttl',
    'category': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/category.ttl',
    'discipline': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/discipline.ttl',
    'educationalRole': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/educationalAudienceRole.ttl',
    'educationalUse': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/educationalUse.ttl',
    'intendedEndUserRole': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/intendedEndUserRole.ttl',
    'interactivityType': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/interactivityType.ttl',
    'learningResourceType': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/learningResourceType.ttl',
    'lifecycleContributeRole': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/lifecycleContributeRole.ttl',
    'rightsCopyrightAndOtherRestrictions': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/rightsCopyrightAndOtherRestrictions.ttl',
    'rightsCost': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/rightsCost.ttl',
    'sourceContentType': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/sourceContentType.ttl'
}


class Vocab(Resource):
  @classmethod
  def get_vocab(cls, name):
    vocabs = []
    # initialize Graph
    graph = rdflib.Graph()
    g = graph.parse(uris.get(name), format="n3")
    g_serialized = g.serialize(format='json-ld', indent=4)
    y = json.loads(g_serialized)

    for item in y:
      try:
        d = {}
        altId = []
        d['id'] = item['@id']
        label = []
        label_de = next(
            (item for item in item['http://www.w3.org/2004/02/skos/core#prefLabel'] if item['@language'] == "de"), None)
        label_en = next(
            (item for item in item['http://www.w3.org/2004/02/skos/core#prefLabel'] if item['@language'] == "en"), None)
        label += [label_de] if label_de is not None else []
        label += [label_en] if label_en is not None else []
        d['label'] = label


        try:
          description = []
          description_de = next(
              (item for item in item['http://www.w3.org/2004/02/skos/core#definition'] if item['@language'] == "de"), None)
          description_en = next(
              (item for item in item['http://www.w3.org/2004/02/skos/core#definition'] if item['@language'] == "en"), None)
          description += [description_de] if description_de is not None else []
          description += [description_en] if description_en is not None else []
          d['description'] = description
        except:
          d['description'] = ''
          print('no description found')
          pass

        try:
          for altLabel in item['http://www.w3.org/2004/02/skos/core#altLabel']:
              altId.append(altLabel)
          d['altId'] = altId
        except:
          d['altId'] = ''
          pass
      except:
          pass
      if d and 'label' in d.keys():
          vocabs.append(d)
    return vocabs

  def get(self, name):
    vocab_dict = self.get_vocab(name)
    return { 
      'vocabs': vocab_dict
      }
