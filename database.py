import pyrebase 
import json
from datetime import datetime,timezone

class DBhandler:
    def __init__(self):
        with open('authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def child(self, node_name):
        return self.db.child(node_name)
    
    # 상품 등록 
    def insert_product(self, userId, data, productImage):
        product_info = {
            "productName" : data ['productName'],
            "price" : data['price'],
            "category":data['category'],
            "location":data['location'],
            "description":data['description'],
            "productImage": productImage,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "reviewCount": 0,
            "userId": userId
        }
        
        product_ref = self.db.child("products").child(userId).push(product_info)
        productId = product_ref['name']
        # print(f"Product ID: {productId} 등록 성공") 
        # print(f"Nickname: {nickname}") #nickname이 넘어오지 않는 상태! 
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
        #print("###########", products)
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
    def insert_review(self, data, img_path):
        # 상품 정보 가져오기 
        productId = data.get("productId")
        product = self.db.child("products").child(productId).get().val() 
        productName = product.get("productName")

        review_info={
            "productId" : data.get("productId"), 
            "productName": productName,
            "userId": data.get("userId"),
            "title": data.get("title"),
            "content": data.get("content"),
            "rate" : int(data.get("reviewStar")),
            "createdAt" : data.get("createdAt", datetime.utcnow().isoformat()),
            "reviewImage": img_path
        }
        self.db.child("reviews").push(review_info)
    
    # 리뷰 전체 조회 
    def get_reviews(self):
        reviews=self.db.child("review").get().val()
        return reviews
    
    # 리뷰 상세 조회
    def get_review_by_id(self, reviewId):
        review = self.db.child("reviews").child(reviewId).get().val()
        return review
    
    # 상품 별 리뷰 상세 조회 
    def get_review_by_product(self, productId):
        # Firebase에서 데이터 가져오기
        allReviews = self.db.child("reviews").get().val()

        # 리뷰가 없으면 빈 리스트와 기본 이미지 반환 
        if not allReviews:
            return [], "default.jpg"
        
        # productId를 기준으로 리뷰 필터링 
        productReviews = [
            {
                "reviewId" : reviewId,
                "rate": int(reviewData.get("reviewStar")),
                "title": reviewData.get("title"),
                "content" : reviewData.get("content"),
                "reviewImage" : reviewData.get("reviewImage"),
            }
            for reviewId, reviewData in allReviews.items()
            if reviewData.get("productId") == productId
        ]

        # 제품 데이터 가져오기 
        productData = self.db.child("products").child(productId).get().val()
        productImage = productData.get("productImage") if productData else "default.jpg"

        # 리뷰와 제품 이미지 반환 
        return productReviews, productImage
    #-----------------------------------------------------------------------------------------  
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
    def find_user(self, userId, pw_hash):
        # 모든 사용자 데이터를 가져옴 
        users = self.db.child("users").get()

        # 모든 사용자 데이터에서 userId와 비밀번호 확인 
        for user in users.each():
            value = user.val()
            if value['userId'] == userId and value['pw'] == pw_hash:
                return value.get('nickname', None)
        return None
    
    # 회원가입 
    def insert_user(self, data, pw_hash):
        user_info ={
        "userId": data['userId'],
        "pw": pw_hash,
        "nickname": data['nickname'],
        "email": data['email'],
        "phoneNum":data['phoneNum'],
        "purchasedProducts" : {} # 빈 구매 목록 
        }

        # nickname을 최상위 키로 사용 
        nickname = data["nickname"] 

        # 사용자 중복 여부 확인 
        if self.user_duplicate_check(nickname):
           self.db.child("users").child(nickname).set(user_info)
           return True
        return False

    # 중복된 사용자 ID 체크 
    def user_duplicate_check(self, id_string):
        users = self.db.child("users").get()
        print("users###",users.val())
        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()
                if 'id'in value and value['id'] == id_string:
                   return False
            return True
    
