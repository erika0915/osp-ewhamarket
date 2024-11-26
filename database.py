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
        products = self.db.child("product").get()
        target_value=""
        #print("###########", name)
        for res in products.each():
            key_value = res.key()
            if key_value == productName:
                target_value = res.val()
        return target_value
#------------------------------------------------------------------------------------------   
    # 리뷰 등록 
    def insert_review(self, productName, data, img_path):
        review_info={
            "userId": data.get("userId"),
            "title": data.get('title'),
            "content": data.get('content'),
            "rate" : data.get('reviewStar'),
            "reviewImage": img_path
        }
        self.db.child("review").child(productName).push(review_info)
    
    # 리뷰 전체 조회 
    def get_reviews(self):
        reviews=self.db.child("review").get().val()
        return reviews
    
    # 리뷰 상세 조회
    def get_review_by_id(self, productName, review_id):
        review = self.db.child("review").child(productName).child(review_id).get().val()
        return review
#------------------------------------------------------------------------------------------  
    def get_heart_byname(self, uid, productName):
        hearts = self.db.child("heart").child(uid).get()
        target_value =""
        if hearts.val() == None:
            return target_value
        
        for res in hearts.each():
            key_value = res.key()
            
            if key_value == productName:
                target_value = res.val()
        return target_value
    
    def update_heart(self, userId, isHeart, productName):
        heart_info={
            "interested" : isHeart
        }
        self.db.child("heart").child(userId).child(productName).set(heart_info)
        return True

#------------------------------------------------------------------------------------------
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
       "nickname": data['nickname'],
       "email": data['email'],
       "phoneNum":data['phoneNum']
        }
        if self.user_duplicate_check(str(data['userId'])):
           self.db.child("user").child(data['userId']).set(user_info)
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
                if 'id'in value and value['id'] == id_string:
                   return False
            return True
    
