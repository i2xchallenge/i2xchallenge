# API Docs

#### Register
	
	Endpont: POST `/api/v1/user/`
	
	username: username of the user, required.
	email: email of user, required.
	password: user's password, required.
	first_name: user's first name, required.
	last_name: user's lastname, required.
	verified: True if user is verified, optional.
	
	Example:
	{
		verified: false,
		user: {
			"username": "DarthVader",
			"password": "deathstar",
			"email": "darth@darkside.com",
			"first_name": "Darth",
			"last_name": "Vader"
			}
	}
	
#### Login

	Endpoint: POST `/api/v1/login/`

	Example:
	{
		"username": "DarthVader",
		"password": "deathstar"
	}

#### Verify Email
	
	Endpoint GET `/api/v1/verify`
		
	GET query params:
		user_id: 121231
		
		Example:
		https://i2x.ai/api/v1/verify/?user_id=121


#### Create Team

	Endpoint POST `/api/v1/team/`
	
	name: Name of team to be created, max_length = 200
	
	Example:
	{
		name: "darkside"
	}


#### Trigger reset password

	Endpoint POST `/api/v1/reset`
	
	Example:
	{
		"email": darth@deathstar.com
    }


#### Reset password
	
	Endpoint POST `/api/v1/password`
	
	Example:
	{
	  'user_id': 1212,
      'new_password': #$@!@!
    }