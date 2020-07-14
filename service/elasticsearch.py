
# from elasticsearch import Elasticsearch
import requests
from requests.auth import HTTPBasicAuth 
import json
from bs4 import BeautifulSoup

def find_product(keyword):
  data = '''
  {
      "query": {
          "query_string" : {
              "query" : "'''+keyword+'''",
              "default_field" : "title"
              }
          },
  "from" : 0,
  "size" : 200 
  }
  '''
  
  data = data.encode('utf-8')
  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  r = requests.get('https://db0e3dae0703454c8c578104428487a6.asia-southeast1.gcp.elastic-cloud.com:9243/ecommerce_title/_search',headers = headers, data=data, auth=HTTPBasicAuth('intentsearch','123456789'))
  #print(r.text)
  results = json.loads(r.text, encoding='utf-8')['hits']['hits']

  product_list = []
  for result in results[::]:
      product_list.append(result['_source']['title'])
  return product_list

if __name__ == "__main__":
  print(find_product('quan'))  