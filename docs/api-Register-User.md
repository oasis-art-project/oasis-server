* **Title**: Create a new user
* **URL**: /api/user/register
* **Method**: POST
* **URL Params**: None

* **Data Params**:  
{  
"email": [string] // Required. Format: email  
"firstName": [string] // Required. minLength: 1  
"lastName": [string] // Required. minLength: 1  
"password": [string] // Required. minLength: 5  
"role": [string] // Required. From 1 to 4 where 1 - Admin, 2 - Host, 3 - Artist, 4 - Visitor. Role 1 can create only a user with the same role  
}  

* **Success response**:  
	* **Code**: 200  
	**Content**: {'ok': True, 'message': 'User created successfully!'}  

* **Error response**:  
	* **Code**: 400  
	**Content**: {'ok': False, 'message': 'Bad request parameters: {}'.format(message)}  
	  
	* **Code**: 400  
	**Content**: {'ok' : False, 'message': 'User already exists'}  
	  
	* **Code**: 401  
	**Content**: {'ok': False, 'message': 'No privileges for creating an admin'}  

* **Sample call**:  
	{  
		"email": "admin@oasis.com",  
		"firstName": "Admin",  
		"lastName": "Admin",  
		"password": "Oasis",  
		"role": 1  
	}  
