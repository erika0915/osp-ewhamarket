from app import create_app  # create_app 함수 가져오기

# Flask 애플리케이션 생성
application = create_app()

# 애플리케이션 실행
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000, debug=True)
