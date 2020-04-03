from flask_restful import Resource, reqparse
import json
import rdflib

# Use the parse functions to point directly at the URI

uris = {
    'educationalRole': 'https://www.dublincore.org/vocabs/educationalAudienceRole.ttl',
    'alignmentType': 'https://www.dublincore.org/vocabs/alignmentType.ttl',
    'educationalUse': 'https://www.dublincore.org/vocabs/educationalUse.ttl',
    'interactivityType': 'https://www.dublincore.org/vocabs/interactivityType.ttl',
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
          d['label'] = item['http://www.w3.org/2004/02/skos/core#prefLabel'][0]['@value']
          try:
            d['description'] = item['http://www.w3.org/2004/02/skos/core#definition'][0]['@value']
          except:
            d['description'] = ''
      except:
          print("not there")
      # only append dict if not empty
      if d:
        vocabs.append(d)
    return vocabs

  def get(self, name):
    vocab_dict = self.get_vocab(name)
    return { 
      'vocabs': vocab_dict
      }
