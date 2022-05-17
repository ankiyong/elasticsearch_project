from datetime import datetime
from pydantic import BaseModel
import uvicorn 
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse 
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates 
from elasticsearch import Elasticsearch

app = FastAPI()
templates = Jinja2Templates(directory="templates") 
app.mount("/static", StaticFiles(directory="static"), name="static") 

@app.get("/", response_class=HTMLResponse) 
async def read_item(request: Request,search_text: str = '코로나', media:str ='' , sort: str = "", start: int = 0, size:int =  10):

	es = Elasticsearch(['https://elastic:123456@192.168.219.141:9200','https://elastic:123456@192.168.219.162:9200'],verify_certs=False,ssl_show_warn=False)

	res = ''

	body = {
		"id": "news_template",
		"params": {
			"input": search_text,
			"media" : media,
			"sort": sort,
			"from" : start,
			"size": size
		}
	}

	try:		
		res = es.search_template(body=body, index='news')
	except Exception as e:
		print(str(e))

	try:
		media = res['hits']['hits'][0]['_source']['media']
	except Exception as e:
		media = ''
	
	total_value = res['hits']['total']['value']
	
	hits = res['hits']['hits']

	result = {
		"request": request, 
		"hits" : hits,
		"search_text" : search_text,
		"media" : media,
		"total_value" : total_value
	}

	return templates.TemplateResponse("item.html", result) 
	#return templates.TemplateResponse("item.html", '') 

if __name__ == '__main__': uvicorn.run(app)
