from flask_restful import Resource, reqparse
import json
import rdflib

# Use the parse functions to point directly at the URI

uris = {
    'educationalRole': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/educationalAudienceRole.ttl',
    ## LRMI path for now pointing to educational Role until vocab is ready
    'intendedEndUserRole': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/educationalAudienceRole.ttl',
    'alignmentType': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/alignmentType.ttl',
    'educationalUse': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/educationalUse.ttl',
    'interactivityType': 'https://raw.githubusercontent.com/sroertgen/oer-metadata-hub-vocab/master/interactivityType.ttl',
    'learningResourceType': 'https://raw.githubusercontent.com/dini-ag-kim/hcrt/master/hcrt.ttl'
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
        label_de = next(
            (item['@value'] for item in item['http://www.w3.org/2004/02/skos/core#prefLabel'] if item['@language'] == "de"), None)
        label_en = next(
            (item['@value'] for item in item['http://www.w3.org/2004/02/skos/core#prefLabel'] if item['@language'] == "en"), None)
        if label_de is not None:
          d['label'] = label_de
          altId.append(label_de)
          if label_en is not None:
            altId.append(label_en)
        else:
          d['label'] = label_en

        try:
          description_de = next(
              (item['@value'] for item in item['http://www.w3.org/2004/02/skos/core#definition'] if item['@language'] == "de"), None)
          description_en = next(
              (item['@value'] for item in item['http://www.w3.org/2004/02/skos/core#definition'] if item['@language'] == "en"), None)
          if description_de is not None:
            d['description'] = description_de
          else:
            d['description'] = description_en
        except:
          d['description'] = ''
          print('no description found')
          pass

        try:
          for altLabel in item['http://www.w3.org/2004/02/skos/core#altLabel']:
              altId.append(altLabel['@value'])
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
