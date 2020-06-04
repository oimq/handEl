## HandEl

##### Mode easily handle the elasticsearch module

for installing and using, requirements are below : 

* tqdm : https://github.com/tqdm/tqdm

* elasticsearch : https://github.com/elastic/elasticsearch-py

***

### Installation

```code
pip3 install handEl-master/
```

***

### Projects

handEl mechanisms are introduce in below.

![hd1](./imgs/hd1.png)

Before we started, if you don't know about elasticsearch,

please study from here : https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html

handEl has several useful functions.

* indexing : Change the index for doing utilies.

* search : Search the document from fields by text or texts.

* tokenize : Using ES analyzer. (you need to make the analyzer for that)

* doc : Search the document from id by text or texts.

* num : Get number of results.

* prope : Create documents from dictionaries.

***

### Examples

* Script
```python3
he = handEl()
he.indexing("handel_test")
he.prope("A", {'alias':['merong', '메롱']}, False, "handel_test")
he.doc("A");         pp(he.result)
he.search("메롱");    pp(he.result)
print(he.tokenize("i you mine want yeah to why put some red shirts"))
```
* Outputs
```python
{'match_num', 'match_sco', 'match_ids', 'match_res'}
{'match_num', 'match_sco', 'match_ids', 'match_res'}
['red', 'shirts']
```

***


### Notices

###### Unauthorized distribution and commercial use are strictly prohibited without the permission of the original author and the related module.