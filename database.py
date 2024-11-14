import pyrebase 
import json 

class DBhandler:
    def __init__(self):
        with open('.github/authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    def insert_item(self, name, data, img_path):
        item_info ={
            "userId":data['userId'],
            "productName" : data ['productName'],
            "price" : data['price'],
            "category":data['category'],
            "option":data['option'],
            "location":data['location'],
            "shortDescription":data['shortDescription'],
            "description":data['description'],
            "img_path":img_path
        }
        self.db.child("item").child(name).set(item_info)
        print(data, img_path)
        return True 

    def insert_user(self, data, pw):
        user_info ={
        "id": data['id'],
        "pw": pw,
       "nickname": data['nickname']
        }
        if self.user_duplicate_check(str(data['id'])):
           self.db.child("user").push(user_info)
           print(data)
           return True
        else:
            return False

    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        print("users###",users.val())
        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()
            if value['id'] == id_string:
                return False
        return True