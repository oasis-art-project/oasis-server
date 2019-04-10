* **Title**: Refresh a user's token
* **URL**: /api/user/refresh
* **Method**: POST
* **URL Params**:   
	**Required** JWT Auth token

* **Data Params**: None 

* **Success response**:  
	* **Code**: 200  
	**Content**: {'ok': True, 'data': ret} 

* **Notes**: 
	ret in the success response is the new token 
