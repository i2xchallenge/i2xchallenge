# Usage

#### Vagrant setup
1. Download and install vagrant and [virtual box](https://www.vagrantup.com/downloads.html) if you do not have it already
2. `>>> vagrant up --provision` 
3. `>>> vagrant ssh`
4. After sshing into vagrant virtual machine run goto <br> `>>> cd /opt/i2x`
5. `>>> python3 manage migrate`
6. `>>> python3 manage.py test` to run test
7. `>>> python3 manage.py runserver 0.0.0.0:9000` to run server
8. Run this from your host machine or from vagrant virtual machine <br> `>>> curl localhost:9000/api/v1/user/`


### Setup on OXS without vagrant and virtualbox
1. Install depencencies <br>`>>> brew install build-essential python3-dev python3-pip sqlite3 libsqlite3-dev git`
2. Create Virtualenv <br>`>>> pip3 install virtualenv i2x_env`
3. Activate virtualenv <br>`>>> ./i2x_env/bin/activate`
2. Install Requiremnts <br>`>>> pip3 install -r requirements.txt`
3. Migrate database <br>`>>> python3 manage.py migrate`
4. Run tests <br>`>>> python3 manage.py test`
5. Run Server <br>`>>> python3 manage.py runserver`
7. Curl <br>`>>> curl localhost:8000/api/v1/user/`


# API Docs

#### Register
	
Endpont: POST `/api/v1/user/`
	
**username**   : username of the user, required. <br>
**email**      : email of user, required. <br>
**password**   : user's password, required. <br>
**first_name** : user's first name, required. <br>
**last_name**  : user's lastname, required. <br>
**verified**   : True if user is verified, required. <br>
	
Example:
```
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
```	
#### Login

Endpoint: POST `/api/v1/login/`

Example:
```
{
    "username": "DarthVader",
    "password": "deathstar"
}
```

#### Verify Email
	
Endpoint GET `/api/v1/verify`
		
GET query params: <br>
**user_id** : <user_id> <br>
		
Example:
        ```https://i2x.ai/api/v1/verify/?user_id=121```


#### Create Team

Endpoint POST `/api/v1/team/` <br>
	
**name**: Name of team to be created, max_length = 200 <br>
	
Example:
```
{
    name: "darkside"
}
```

#### Trigger reset password

Endpoint POST `/api/v1/reset`
	
Example:
```
{
    "email": darth@deathstar.com
}
```

#### Reset password
	
Endpoint POST `/api/v1/password`
	
Example:
```
{
    'user_id': 1212,
    'new_password': #$@!@!
}
```
