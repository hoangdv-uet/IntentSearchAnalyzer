import json
from flask import Flask, escape, request, render_template, Response
from service.elasticsearch import find_product
from service.tag_extraction import get_entity_by_tag, load_model

models = {}
models["target_model"] = load_model("./service/model/final-model-target.pt")
models["non_target_model"] = load_model("./service/model/final-model-non-target.pt")

app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def hello():
    return render_template('index.html')

@app.route('/ajaxhandler', methods = ['POST','GET'])
def process_products():
    xml = ''
    keyword = request.form.get('keyword')
    product_list = find_product(keyword)
    return json.dumps(product_list)


@app.route('/model', methods = ['POST','GET'])
def home():    
    return render_template('index_.html')

@app.route('/ajaxhandlermodel', methods = ['POST','GET'])
def process_products_model():
    xml = ''
    keyword = request.form.get('keyword')
    tagged_sentences, tag_dict = get_entity_by_tag(query=keyword, models=models)
    #print(tag_dict)
    str1 = keyword.replace(' '.join(tag_dict['TARGET']),"(" +' '.join(tag_dict['TARGET'])+")^2")
    product_list = find_product(str1)
    print(str1)
    return json.dumps({"tagged_sentences": tagged_sentences, "product_list": product_list})

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=63500)