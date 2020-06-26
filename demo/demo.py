from handEl import handEl
from pprint import pprint as pp

if __name__ == "__main__" :
    HOST = 'localhost'
    PORT = 8080

    INDEX = "test_index"
    DATA1 = {'alias':['hello', '메롱']}
    DATA2 = {'alias':['world', '메렁']}

    he = handEl(host=HOST, port=PORT)
    # Index from the ES
    he.indexing(INDEX)   

    # Add documents
    he.prope('A0', DATA1, True)
    he.prope("A1", DATA2, False)
    he.doc('A0')
    pp(he.result)
    
    he.search("메롱 좀 하지마!")
    pp(he.result)
    he.search("그럼 메렁 해야지~")
    pp(he.result)

    print(he.tokenize("i might love with you."))