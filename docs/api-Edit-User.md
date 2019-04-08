* **Title**: Editing of a user
* **URL**: /api/user/edit
* **Method**: POST
* **URL Params**:  
  **Required** JWT Auth token  

* **Data Params**:  
{  
"email": [string] // Required. Format: email  
"firstName": [string] // Required. minLength: 1  
"lastName": [string] // Required. minLength: 1  
"password": [string] // minLength: 5  
"role": [numeric] // Required. min 1, max 4  
}  

* **Success response**:  
	* **Code**: 200  
	**Content**: {'ok': True, 'message': 'User has been edited successfully!'}  

* **Error response**:  
	* **Code**: 400  
	**Content**: {'ok': False, 'message': 'Bad request parameters: {}'.format(message)}  
	  
	* **Code**: 400  
	**Content**: {'ok' : False, 'message': 'User doesn\'t exist'}  
	  
	* **Code**: 401  
	**Content**: {'ok': False, 'message': 'No privileges for editing this user'}  

	* **Code**: 401  
	**Content**: {'ok': False, 'message': 'No privileges to make this user an admin'}

	* **Code**: 400  
	**Content**: {'ok': False, 'message': 'Something went wrong'}
	
* **Sample call**:  
	{  
		"email": "admin@oasis.com",  
		"firstName": "Admin",  
		"lastName": "Admin",  
		"role": 1  
	} 

* **Notes**:  
Password is not required for updating. A user could be edited only by the user himself or by an admin (Role 1). Assign admin priveleges can only another admin.
