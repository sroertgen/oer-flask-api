from flask_restful import Resource, reqparse
import json
from rdflib import Graph, SKOS, URIRef


# load the vocab uris
with open('vocabulary.json', 'r') as f:
    uris = json.load(f)


class Vocab(Resource):
    @classmethod
    def get_vocab(cls, name):
        vocabs = []
        # initialize Graph
        graph = Graph()
        g = graph.parse(uris.get(name), format="n3")
        g_serialized = g.serialize(format='json-ld', indent=4)
        y = json.loads(g_serialized)

        for item in y:
            try:
                d = {}
                d['id'] = item['@id']
                label = []
                label_de = next(
                    (item for item in item['http://www.w3.org/2004/02/skos/core#prefLabel'] if item['@language'] == "de"), None)
                label_en = next(
                    (item for item in item['http://www.w3.org/2004/02/skos/core#prefLabel'] if item['@language'] == "en" or item['@language'] == "en-US"), None)
                label += [label_de] if label_de is not None else []
                label += [label_en] if label_en is not None else []
                d['label'] = label
            except:
                pass

            try:
                description = []
                description_de = next(
                    (item for item in item['http://www.w3.org/2004/02/skos/core#definition'] if item['@language'] == "de"), None)
                description_en = next(
                    (item for item in item['http://www.w3.org/2004/02/skos/core#definition'] if item['@language'] == "en" or item['@language'] == "en-US"), None)
                description += [description_de] if description_de is not None else []
                description += [description_en] if description_en is not None else []
                d['description'] = description
            except:
                d['description'] = ''
                pass

            try:
                altId = []
                for altLabel in item['http://www.w3.org/2004/02/skos/core#altLabel']:
                    altId.append(altLabel)
                d['altId'] = altId
            except:
                d['altId'] = ''
                pass

            # try getting parents if a available
            try:
                subject = item['@id']
                parents = {}
                parents['all'] = []
                parents = cls.get_parents(g, subject, parents, 0)

                d['parents'] = parents
            except:
                d['parents'] = ''
                pass

            if d and 'label' in d.keys():
                vocabs.append(d)
        return vocabs

    # function for checking for parents
    @classmethod
    def get_parents(cls, graph, subject, parents, iteration):
        for s, p, o in graph.triples((URIRef(subject), SKOS.broader, None)):
            if iteration == 0:
                parents['direct'] = o
            else:
                parents['all'].append(o)
            iteration += 1
            return cls.get_parents(graph, o, parents, iteration)
        parents['all'].append(parents['direct'])
        return parents

    def get(self, name):
        vocab_dict = self.get_vocab(name)
        return {
            'vocabs': vocab_dict
        }
