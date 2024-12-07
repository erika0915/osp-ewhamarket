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
    
    #------------------------------------------------------------------------------------------   
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
            "purchaseCount":0,
            "reviewCount": 0,
            "userId": userId
        }
        
        product_ref = self.db.child("products").child(userId).push(product_info)
        productId = product_ref['name']
        return productId 
    

    # 상품 전체 조회 
    def get_products(self):
        products = self.db.child("products").get().val()
        flat_products={}
        for userId, userProducts in products.items():
            for productId, productData in userProducts.items():
                flat_products[productId] = productData
        return flat_products
    

    # 상품 상세 조회 : productId로 조회
    def get_product_by_id(self, productId):
        products = self.db.child("products").get().val()

        if not products:
            print("no products found in database")

        for userId, userProducts in products.items():
            if productId in userProducts:
                return userProducts[productId]
        return None
    
    
    # 상품 상세 조회 : productName 조회       
    def get_product_by_productName(self, productName):
        products = self.db.child("products").get()

        for user_id, user_products in products.val().items():
            for product_id, product_info in user_products.items():
                if product_info.get("productName") == productName:
                    return product_info
        return None
 

    # 상품 전체 조회 : 카테고리 조회 
    def get_products_by_category(self, cate):
        items = self.db.child("products").get()
        target_value=[]
        target_key=[]
        for user in items.each():  
            user_data = user.val()  
            for product_key, product_value in user_data.items():  
                if product_value.get("category") == cate:  
                    target_value.append(product_value)
                    target_key.append(product_key)
        new_dict={}
        for k,v in zip(target_key,target_value):
            new_dict[k]=v
        return new_dict
    

    # 데이터베이스에서 특정 상품정보 업데이트
    def update_product(self, productId, updated_data):
        products = self.db.child("products").get()
        for userId, userProducts in products.val().items():
            if productId in userProducts:
                self.db.child("products").child(userId).child(productId).update(updated_data)
                return True
        return None
    

    # 구매 정보를 사용자 데이터에 집어넣기
    def add_purchased_product(self, user_id, product_info,product_id):
        user = self.db.child("users").child(user_id).get()
        purchased_products = user.val().get("purchasedProducts", {})
        product_info["purchaseTime"] = datetime.now(timezone.utc).isoformat()
        product_info["productId"] = product_id  # 여기에 productId 추가
        product_num = f"product_{len(purchased_products) + 1}"
        purchased_products[product_num] = product_info

        self.db.child("users").child(user_id).update({"purchasedProducts": purchased_products})
        return True
    
    # 사용자 데이터 가져오기
    def update_purchased_product_review(self, userId, productId, reviewId):
        user = self.db.child("users").child(userId).get().val()
        if not user:
            print(f"Debug: User {userId} not found.")
            return False

        # purchasedProducts 데이터 업데이트
        purchased_products = user.get("purchasedProducts", {})
        for product_key, product_data in purchased_products.items():
            if product_data.get("productId") == productId:
                self.db.child("users").child(userId).child("purchasedProducts").child(product_key).update({"reviewId": reviewId})
                return True

        print(f"Debug: Product {productId} not found in user's purchased products.")
        return False
    
    #------------------------------------------------------------------------------------------   
    # 리뷰 등록 
    def insert_review(self, data, img_path):
        # 상품 정보 가져오기 
        productId = data.get("productId")
        product = self.db.child("products").child(productId).get().val() 

        # 사용자 정보 가져오기 
        userId = data.get("userId")
        user=self.db.child("users").child(userId).get().val()
        nickname = user.get("nickname")

        # 리뷰 데이터 생성 
        review_info={
            "productId" : productId,
            "userId": userId,
            "title": data.get("title"),
            "content": data.get("content"),
            "rate" : data.get("rate"),
            "nickname" : nickname,
            "createdAt" : data.get("createdAt", datetime.utcnow().isoformat()),
            "reviewImage": img_path
        }
        review_ref=self.db.child("reviews").push(review_info)
        reviewId = review_ref['name']
        return reviewId


    # 리뷰 전체 조회 
    def get_reviews(self):
        reviews=self.db.child("reviews").get().val()
        return reviews
    
    # 리뷰 상세 조회
    def get_review_by_id(self, reviewId):
        all_reviews = self.db.child("reviews").get().val()
        if all_reviews and reviewId in all_reviews:
            review = all_reviews[reviewId]

            # 날짜 변환 
            createdAt = review.get("createdAt")
            if createdAt:
                review["createdAt"] = datetime.fromisoformat(createdAt).date()
            return review
        return None
    
    # 상품 별 리뷰 목록 조회 
    def get_review_by_product(self, productId):
        allReviews = self.db.child("reviews").get().val()
        if not allReviews:
            return []  

        productReviews = []
        for reviewId, reviewData in allReviews.items():
            if reviewData.get("productId") == productId: 
                # 날짜 추출
                created_at = reviewData.get("createdAt")
                if created_at:
                    created_at=datetime.fromisoformat(created_at).date()

                productReviews.append({
                    "reviewId": reviewId,
                    "userId": reviewData.get("userId"),
                    "rate": reviewData.get("rate"),
                    "title": reviewData.get("title"),
                    "nickname" : reviewData.get("nickname"), 
                    "content": reviewData.get("content"), 
                    "reviewImage": reviewData.get("reviewImage"),  
                    "createdAt": created_at,
                })
        return productReviews
    #-----------------------------------------------------------------------------------------  
    # 좋아요 상태 조회 
    def get_heart_by_Id(self, userId, productId):
        hearts = self.db.child("hearts").child(userId).child(productId).get().val()
        return hearts if hearts else {"interested": "N"}
    
    # 좋아요 상태 업데이트 
    def update_heart(self, userId, productId, isHeart):
        heart_info={
            "interested" : isHeart
        }
        self.db.child("hearts").child(userId).child(productId).set(heart_info)
        save_data = self.db.child("hearts").child(userId).child(productId).get().val()
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
    def insert_user(self, data, pw_hash, profile_image):
        user_info ={
        "userId": data['userId'],
        "pw": pw_hash,
        "nickname": data['nickname'],
        "name":data['name'],
        "email": data['email'],
        "phoneNum":data['phoneNum'],
        "bday":data['bday'],
        "profileImage": profile_image,
        "purchasedProducts" : {} # 빈 구매 목록 
        }

        # 사용자 중복 여부 확인 
        if self.user_duplicate_check(data['userId']):
           self.db.child("users").child(data['userId']).set(user_info)
           return True
        return False


    # 중복된 사용자 ID 체크 
    def user_duplicate_check(self, userId):
        user = self.db.child("users").child(userId).get().val()
        if user:
            return False
        return True
    
    # 중복된 nickname 체크
    def nickname_duplicate_check(self, nickname):
        # users 경로에서 모든 데이터를 가져옵니다.
        users = self.db.child("users").get().val()

        # 데이터가 없으면 중복될 가능성이 없으므로 True 반환
        if not users:
            return True

        # 모든 userid를 순회하며 nickname 확인
        for userid, user_data in users.items():
            if user_data.get("nickname") == nickname:  # nickname이 중복되면 False 반환
                return False
        return True 
    
    # 사용자 정보 ID로 가져오기 
    def get_user_by_id(self, userId):
        user= self.db.child("users").child(userId).get().val()
        return user
    #------------------------------------------------------------------------------------------
    # 마이페이지 
    # 사용자 정보 조회 
    def get_user_info(self, userId):
        user= self.db.child("users").child(userId).get().val()
        if not user:
            return None 
        return{
            "nickname":user.get("nickname"),
            "email":user.get("email"),
            "profileImage": user.get("profileImage"),
            "phoneNum" : user.get("phoneNum"),
            "userId" : user.get("userId"),
        }
    
    # 구매 목록 조회 
    def get_purchased_list(self, userId):
        userPurchased = self.db.child("users").child(userId).child("purchasedProducts").get().val()

        # 구매 목록이 없으면 빈 리스트 반환 
        if not userPurchased:
            return []
        
        # 구매 목록 반환 
        return[
            {
                "productId" : item.get("productId"),
                "productName" : item.get("productName"),
                "productImage":item.get("productImage")
            }
            for item in userPurchased.values()
        ]

    # 판매 목록 조회 
    def get_sell_list(self, userId):
        # 사용자가 등록한 상품 데이터 가져오기 
        products = self.db.child("products").child(userId).get().val()

        # 등록된 상품이 없으면 빈 리스트 반환 
        if not products:
            return []
        # 상품 목록을 리스트로 변환 
        return[
            {   
                "productId" : productId,
                "productName" : productData.get("productName"),
                "productImage": productData.get("productImage")
            }
            for productId, productData  in products.items()
        ]
    
    # 좋아요 목록 
    def get_heart_list(self, userId):
        hearts = self.db.child("hearts").child(userId).get().val()

        if not hearts:
            return []

        heart_list = []
        for productId, heartData in hearts.items():
            if heartData.get("interested") == 'Y':
                products = self.db.child("products").get().val()

                if not products:
                    continue

                for userId, userProducts in products.items():
                    if productId in userProducts:
                        product = userProducts[productId]
                        heart_list.append({
                            "productId": productId,
                            "productName": product.get("productName"),
                            "productImage": product.get("productImage"),
                            "interested": heartData.get("interested")
                        })
                        break

        print(f"[DEBUG] Heart list: {heart_list}")
        return heart_list
        
    # 닉네임으로 사용자 정보 조회
    def get_user_info_by_nickname(self, nickname):
        users = self.db.child("users").get()
        for user in users.each():
            user_data = user.val()
            if user_data.get("nickname") == nickname:  # 닉네임이 일치하는 경우
                return {
                    "nickname": user_data.get("nickname"),
                    "email": user_data.get("email"),
                    "profileImage": user_data.get("profileImage"),
                    "phoneNum": user_data.get("phoneNum"),
                    "userId": user.key()  # userId는 상위 키로 저장됨
                }