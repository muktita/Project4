# 449wordleproject1

### Group Members:
##### Fenil Ketan Bhimani
##### Parth Sharma
##### Rakesh Singh
##### Jarrod Leong

## **Initializing Database & Start Service:**
##### copy 'wordleauth' into your nginx directory (/etc/nginx/sites-enabled/)
##### restart nginx `sudo service nginx restart`
##### navigate to project directory
##### `cd src/database`
##### `python3 setupDB.py`  *use `setupDB.py -p` to populate the database*
##### `cd ..`
##### `foreman start --formation game=3,user=1`

---

## **Testing the APIs**

#### *Can test using user-id: 123abc and username: user1.  Username is not checked but included for redundancy*
#### *includes games g1 and g2 as test games.  game_ids are shortend here for ease of use but are uuids in game*
#### *make sure to use the correct user-id.  Supplying an incorrect user-id after you have logged in will result in resources not being found as username and user-id will not match. When using /game/create you will be able to create games even with an incorrect user-id but you will not be able to access them.*

### **Register Username & Password**
##### `http POST http://tuffix-vm/register username=<username> password=<password>`

### **Create a Game**
##### `http POST http://tuffix-vm/game/create user-id:<user-id> username:<username> -a <username>:<password>`

### **Input Word Guess**
##### `http POST http://tuffix-vm/game/guess user-id:<user-id> username:<username> game_id=<game_id> guess=<guess> -a <username>:<password>`

### **List All Games in Progress**
##### `http GET http://tuffix-vm/game/list user-id:<user-id> username:<username> -a <username>:<password>`

### **List a Specific Game in Progress**
##### `http GET http://tuffix-vm/game/{game_id} user-id:<user-id> username:<username> -a <username>:<password>`














