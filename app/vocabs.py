from flask_restful import Resource, reqparse
import json
import rdflib


# load the vocab uris
with open('vocabulary.json', 'r') as f:
    uris = json.load(f)


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
