function id_overlap_check() {
    const usernameInput = document.getElementById('mkId');
    const username = usernameInput.value.trim();
	
    if (username.length == 0){
    	alert('아이디를 입력하세요');
        usernameInput.setAttribute('check_result', 'fail');
        return;
    }

    if (username.length < 6 || username.length > 20) {
        alert('아이디는 6-20자 사이여야 합니다.');
        usernameInput.setAttribute('check_result', 'fail');
        return;
    }

    //데이터베이스 연결
    const database = firebase.database();
    const usersRef = database.ref('user');

    // 중복 확인 체크
    usersRef.once('value')
        .then((snapshot) => {
            const users = snapshot.val();
            
            // 없으면 
            if (users === null) {
                alert('사용 가능한 아이디입니다.');
                usernameInput.setAttribute('check_result', 'success');
                return;
            }

            // 있으면
            let isDuplicate = false;
            Object.values(users).forEach(user => {
                if (user.id === username) {
                    isDuplicate = true;
                }
            });

            if (isDuplicate) {
                alert('이미 존재하는 아이디입니다.');
                usernameInput.setAttribute('check_result', 'fail');
            } else {
                alert('사용 가능한 아이디입니다.');
                usernameInput.setAttribute('check_result', 'success');
            }
        })

        //에러 발생 처리 
        .catch((error) => {
            console.error('Username check error:', error);
            alert('오류가 발생했습니다. 다시 시도해주세요.');
            usernameInput.setAttribute('check_result', 'fail');
        });
}

function pushRegiButton(){
	alert("등록되었습니다");
}

function pushResetButton(){
	alert("취소되었습니다");
}