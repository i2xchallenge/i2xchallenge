# Usage

### Vagrant setup
	1. Download and install vagrant and [virtual box] (https://www.vagrantup.com/downloads.html) if you do not have it already
	2. `>>> vagrant up --provision` 
	3. `>>> vagrant ssh`
	4. After sshing into vagrant virtual machine run goto `>>> cd /opt/i2x`
	5. `>>> python3 manage migrate`
	6. `>>> python3 manage.py test` to run test
	7. `>>> python3 manage.py runserver` to run server
	8. Run this from your host machine or from vagrant virtual machine `>>> curl localhost:8000/api/v1/user/`


### Setup on OXS without vagrant and virtualbox
	1. Install depencencies `>>> brew install build-essential python3-dev python3-pip sqlite3 libsqlite3-dev git`
	2. Create Virtualenv `>>> pip3 install virtualenv i2x_env`
	3. Activate virtualenv `>>> ./i2x_env/bin/activate`
	2. Install Requiremnts `>>> pip3 install -r requirements.txt`
	3. Migrate database `>>> python3 manage.py migrate`
	4. Run tests `>>> python3 manage.py test`
	5. Run Server `>>> python3 manage.py runserver`
	7. Curl `>>> curl localhost:8000/api/v1/user/`


# API Docs

#### Register
	
	Endpont: POST `/api/v1/user/`
	
	username   : username of the user, required.
	email      : email of user, required.
	password   : user's password, required.
	first_name : user's first name, required.
	last_name  : user's lastname, required.
	verified   : True if user is verified, optional.
	
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
		user_id : 121231
		
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
