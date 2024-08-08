from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from middlewares.error404 import Error404Middleware
from modules.uploadImage import UploadImage
import uvicorn

app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(
	Error404Middleware
)
app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_methods=['*'],
	allow_headers=['*']
)

@app.get('/', tags=['Default'], name='Root', status_code=301)
def root():
	return RedirectResponse('/docs')

@app.get('/error404', tags=['Default'], name='Error 404', status_code=200)
def root():
	return HTMLResponse(
		content='''
			<div style="display:flex;align-items:center;justify-content:center;width:100%;height:100%;">
				<h3>Page not found!</h3>
			</div>
		'''
	)

@app.post('/upload_image', tags=['API'], name='Upload image to bucket', status_code=200)
def upload_image(url: str = Query(...)):
	response_json = {
		'status': 'error',
		'err_description': ''
	}

	try:
		run_request = UploadImage.run(url)
		response_json = run_request.copy()

	except Exception as e:
		response_json['err_description'] = str(e)

	return JSONResponse(content=response_json)

if __name__ == '__main__':
	uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)