# Uncash Api

this api is used by the uncash services android app its deployed on heroku cloud service 
and deals with postgresql database it has some calls that helps the app to provide the service to the end users .



### Api calls example : signup calls
1. "signup/authentication"

        Method : Post
		returns a  jwt that the app uses to perform the user tasks 
		takes parameters for accessing the api : app_username  , password 
		Response codes : 200 success , 400 mising parameter , 401 bad username or       password
		
1. "signup/verify_phone"

        Method : Post
		takes parameters to verify the new account phone  : jwt as a header  , phone       number
		Response codes : 200 success , 400 mising parameter , 409 conflict phone exists 
		
		
1. "signup/verify_code

        Method : Post
		takes parameters for verifying the number  :jwt as a header , code   and phone number
		Response codes : 200 success , 400 mising parameter , 410 expired code


1. "signup/create_account"

        Method : Post
		returns the id of the created user 
		takes parameters for creating new account  : jwt as a header ,  username  , password  , role ,  phone number 
		Response codes : 200 success , 400 mising parameter , 401 bad username or       password



### Heroku services 
this api is hosted on the heroku services with the postgresql database .

### Uncash Database

consists of 10 tables this is an example :

1. "user"
store the user information 
        id  numeric ,
	username Varchar(10),
	password hash Varchar (120) ,
	role Varchar(10),
	phone number Varchar(11)


1. "storeInfo"
store the information of each store that provide the service 
        id  numeric ,
	name Varchar(10),
	phone number Varchar(11)



the api works with the database using SQLAhcemy ORM  here is the implementaion of the above two tables 

```python
class StoreInfo(db.Model):
    __tablename__ = 'storeinfo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)

```



```python
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)
```


URL : https://uncashapp.herokuapp.com/

Author : Mohammed khidr 
Linkedin : https://www.linkedin.com/in/mohamed-abbas-604999150/







