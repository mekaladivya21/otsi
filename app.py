from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch()
#es.indices.create(index='test-index', ignore=400)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(
        index="moviesnew", 
        size=600, 
        body={
				"query": {
					"multi_match" : {
						"query": search_term, 
							"fields": [
								"Director_name", 
								"Actor_2_name",
								"Genres", 
								"Actor_1_name",
								"Movie_title", 
								"Country"
							] 
					}
				},
				"highlight": {
					"fields" : {
						"Director_name": {}, 
						"Actor_2_name": {},
						"Genres": {}, 
						"Actor_1_name": {},
						"Movie_title": {}, 
						"Country": {}
					}
				}
			}
	)
    return render_template('results.html', res=res )
  
   
@app.route('/search/results', methods=['GET', 'POST'])
def filters_request():
	search_term = request.form["input"]
	filters_term=request.form["radios"]
	if(filters_term=="None"):
		res = es.search(
        index="moviesnew", 
        size=600, 
        body={
				"query": {
					"multi_match" : {
						"query": search_term, 
							"fields": [
								"Director_name", 
								"Actor_2_name",
								"Genres", 
								"Actor_1_name",
								"Movie_title", 
								"Country"
							] 
					}
				}
			}
		)
		return render_template('results.html', res=res )
	else:
		res = es.search(
			index="moviesnew", 
			size=600, 
			body={
				"query": {
					"bool":{
						"must":{
						
							"multi_match" : {
								"query": search_term, 
									"fields": [
										"Director_name", 
										"Actor_2_name",
										"Genres", 
										"Actor_1_name",
										"Movie_title", 
										"Country"
									] 
							}
						},
						    "filter":{
							    "bool":{
                                  "should":[
						               {"match":{"Genres": filters_term}},
                                      {"match":{"Country": filters_term}}
                                   ],
								   "minimum_should_match":1
                                }
						    }
						
					
					}
				}
			}
		)
		return render_template('results.html', res=res )
	
		

if __name__ == '__main__':
	app.secret_key = 'mysecret'
	app.debug = True
	app.run(host='127.0.0.1', port=8082)
