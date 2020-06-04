from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import json
import pprint
from tqdm import tqdm
pp = pprint.pprint

class handEl :
    def __init__(self, host='localhost', port='9200', index="default", props=None) :
        self.es = Elasticsearch(host=host, port=port)
        print("Elasticsearch Connection Success [{}:{}]".format(host, port))
        self.ies = IndicesClient(self.es)
        self.host = host
        self.port = port
        self.index = index
        self.result = None
        self.response = None
        self.props = props
    
    def __str__(self) :
        return "\nDescriptions for handEl\nhost : {}, port : {}, index : {}\ncurrent result : {}\n" \
                .format(self.host, self.port, self.index, self.result)
    
    def __call__(self) :
        print("\nCurrent response ▼")
        pp(self.response) 

    def indexing(self, index) :
        self.index = index

    def search(self, value, index=None, field="alias", fuzziness=0) :
        if index : self.indexing(index)
        if self.match(value, field=field, fuzziness=fuzziness) :
                return self.result
        else :  return None

    def tokenize(self, value, tokenizer="natural_tokenizer") :
        if not value : return []
        tokens = self.ies.analyze(index=tokenizer, body={"field":"comments", "text":value})
        if tokens['tokens'] : return [token['token'] for token in tokens['tokens']]
        else                : return []

    def match(self, value, field="alias", fuzziness=0) :
        body = {"query" : {"match": {field : {"query":value, "fuzziness":fuzziness}}}} 
        return self.parse(self.es.search(index=self.index, body=body))

    def parse(self, res, score=1.0) :
        self.response = res
        if res["hits"]["total"]["value"] > 0 :
            self.result = {
                'match_num':res["hits"]["total"]["value"],
                'match_sco':res["hits"]["max_score"],
                'match_ids':[hit["_id"] for hit in res["hits"]["hits"]],
                'match_res':[hit["_source"] for hit in res["hits"]["hits"]],
            }
            return True
        else : 
            self.result = None
            return False

    def doc(self, docid) :
        if self.es.exists(index=self.index, id=docid) :
            res = self.es.get(index=self.index, id=docid)
            self.result = {
                'match_num':1,
                'match_sco':res["_primary_term"],
                'match_ids':[res["_id"]],
                'match_res':res["_source"],
            }
            return True
        else :
            self.result = None
            return False
        
    def num(self) :
        return self.results['match_num']
        
    # Create id - documents
    def prope(self, docid, documents, overturn=False, index=False) :
        try :
            if type(documents) != type(dict()) : raise Exception("The type of contents is not dictionaries!")
            if index            :   self.indexing(index)
            if self.doc(docid)  :   self.update(docid, documents, overturn)
            else                :   self.create(docid, documents)
        except Exception as e :
            self.error(e, "PROPE")

    def unionDict(self, dict0, dict1, appending=True) :
        if appending :
            for k,v in list(filter(lambda x:type(x[1])==type([]), dict0.items())) : dict1[k] = list(set(dict1[k]+v))
        dict0.update(dict1)
        return dict0
            
    def update(self, docid, documents, overturn=False) :
        try :
            if type(documents) != type(dict()) : raise Exception("The type of contents is not dictionaries!")
            if overturn :
                self.es.update(index=self.index, id=docid, body={
                    'doc':{**documents}
                })
            else :
                pp(self.unionDict(self.result['match_res'], documents))
                self.es.update(index=self.index, id=self.result['match_ids'], body={
                    'doc':{**self.unionDict(self.result['match_res'], documents)}
                })
        except Exception as e :
            self.error(e, "UPDATE")

    def create(self, docid, documents) :
        try :
            if type(documents) != type(dict()) : raise Exception("The type of contents is not dictionaries!")
            self.es.create(index=self.index, id=docid, body={**documents})
        except Exception as e :
            self.error(e, "CREATE")

    def error(self, e, msg="") :
        print("ERROR {} : {}".format(msg, e))

if __name__ == "__main__" :
    he = handEl()