* **Title**: Authentication of a user
* **URL**: /api/user/auth
* **Method**: POST
* **URL Params**: None

* **Data Params**:  
{  
"email": [string] // Required. Format: email    
"password": [string] // Required. minLength: 5  
}  

* **Success response**:  
	* **Code**: 200  
	**Content**: {'ok': True, 'data': jsondata} 

* **Error response**:  
	* **Code**: 400  
	**Content**: {'ok': False, 'message': 'Bad request parameters: {}'.format(message)}  
	  
	* **Code**: 401  
	**Content**:  {'ok': False, 'message': 'Invalid username or password'}'

* **Sample call**:  
	{  
		"email": "admin@oasis.com",  
		"password": "Oasis"  
	}

* **Sample return**:  
      "data": {  
        "email": "admin@oasis.com",  
        "first_name": "Admin",  
        "id": 27,  
        "last_name": "Admin",  
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTQ3NDEzNDEsIm5iZiI6MTU1NDc0MTM0MSwianRpIjoiN2IwOTkxODctMDA1Yy00MGE3LTgwNDAtM2I0YjUyZDIxOGZmIiwiZXhwIjoxNTU3MzMzMzQxLCJpZGVudGl0eSI6eyJlbWFpbCI6IjEyMzEyM0AxMjMxMjMuY29tIiwicGFzc3dvcmQiOiJ0ZXN0MTIzIn0sInR5cGUiOiJyZWZyZXNoIn0.WEsDz57JHfudhln_ngHAg6RqMfMhXqEfej0HxWhFQPI",  
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTQ3NDEzNDEsIm5iZiI6MTU1NDc0MTM0MSwianRpIjoiOWYxZTJjODctOGFmMC00NDRjLThlM2MtMTBjOTMzMzU1MmY1IiwiZXhwIjoxNTU0ODI3NzQxLCJpZGVudGl0eSI6eyJlbWFpbCI6IjEyMzEyM0AxMjMxMjMuY29tIiwicGFzc3dvcmQiOiJ0ZXN0MTIzIn0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.Lr6s_gMbkZ8-KY7AFheh8ubPshv45E0n21mMQebSpWM",  
        "user_role": 1  
    },  
    "ok": true

* **Notes**:
	Jsondata in a successful response is json object with user's data. It has two important fields: token and refresh. Both of them have to be saved in HttpOnly cookies since Token contains information about identity and Refresh is necessary for refreshing a token. 

 
