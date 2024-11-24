import pyrebase 
import json 

class DBhandler:
    def __init__(self):
        with open('authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    # 상품 등록 
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
    
    # 상품 전체 조회 
    def get_items(self):
        items = self.db.child("item").get().val()
        return items
    
    # 상품 세부 조회 -> 이름으로 조회 
    def get_item_byname(self, name):
        items = self.db.child("item").get()
        target_value=""
        print("###########", name)
        for res in items.each():
            key_value = res.key()
            
            if key_value == name:
                target_value = res.val()
        return target_value
    
    # 로그인 검증 
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return True
        return False
    
        # 회원가입 
    def insert_user(self, data, pw):
        user_info ={
        "id": data['userId'],
        "pw": pw,
       "nickname": data['nickname']
        }
        if self.user_duplicate_check(str(data['userId'])):
           self.db.child("user").push(user_info)
           print(data)
           return True
        else:
            return False

    # 중복된 사용자 ID 체크 
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
    