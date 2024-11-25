import pyrebase 
import json 

class DBhandler:
    def __init__(self):
        with open('authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    # 상품 등록 
    def insert_product(self, name, data, productImage):
        product_info = {
            "nickname": data ['nickname'],
            "productName" : data ['productName'],
            "price" : data['price'],
            "category":data['category'],
            "location":data['location'],
            "description":data['description'],
            "productImage": productImage
        }
        self.db.child("product").child(name).set(product_info)
        print(data, productImage)
        return True 
    
    # 상품 전체 조회 
    def get_products(self):
        products = self.db.child("product").get().val()
        return products
    
    # 상품 세부 조회 -> 이름으로 조회 
    def get_product_byname(self, productName):
        items = self.db.child("product").get()
        target_value=""
        #print("###########", name)
        for res in products.each():
            key_value = res.key()
            if key_value == productName:
                target_value = res.val()
        return target_value
    
    # 리뷰 등록 
    def insert_review(self, productName, userId, data, img_path):
        review_info={
            "title": data['title'],
            "content": data['content'],
            "rate" : data['rate'],
            "reviewImage": img_path
        }
        self.db.child("review").child(productName).child(userId).set(review_info)
        return True
    
    # 리뷰 전체 조회 
    def get_reviews(self):
        reviews=self.db.child("review").get().val()
        return reviews
    
    # 리뷰 상세 조회 -> 상품명으로 조회 
    def get_review_byname(self, productName):
        reviews=self.db.child("review").child(productName).get().val()
        return reviews

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
    