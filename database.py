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

    #카테고리별 상품리스트 보여주기
    def get_products_bycategory(self, cate):
        items = self.db.child("product").get()
        target_value=[]
        target_key=[]
        for res in items.each():
            value = res.val()
            key_value = res.key()
            if value['category'] == cate:
                target_value.append(value)
                target_key.append(key_value)
        print("######target_value",target_value)
        new_dict={}
        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict
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
        review['productName']=productName
        return review
    
    # 상품 별 리뷰 상세 조회 
    def get_review_by_name(self, productName):
        # Firebase에서 데이터 가져오기
        reviews = self.db.child("review").child(productName).get().val()
        product_data = self.db.child("product").child(productName).get().val()

        # 리뷰 데이터 처리
        if not reviews:
            reviews = []  # 리뷰가 없으면 빈 리스트 반환
        else:
            reviews = [
                {
                    "review_id": review_id,
                    "rate": int(review_data.get("rate", 0)),  # 문자열을 정수로 변환
                    "title": review_data.get("title"),
                    "content": review_data.get("content"),
                    "reviewImage": review_data.get("reviewImage"),
                }
                for review_id, review_data in reviews.items()
            ]

        # 제품 이미지 처리
        product_image = product_data.get("productImage") if product_data else "default.jpg"
        # 두 값을 함께 반환
        return reviews, product_image
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
    
