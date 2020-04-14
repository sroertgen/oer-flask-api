from flask_restful import Resource, reqparse
import json
import rdflib


# load the vocab uris
with open('vocabulary.json', 'r') as f:
    uris = json.load(f)


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

