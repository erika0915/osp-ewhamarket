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

    // 중복 확인 체크
    $.ajax({
        url: '/check_duplicate',
        type: 'POST',
        data: { username: username },
        success: function(response) {
            if (response.available) {
                alert('사용 가능한 아이디입니다.');
                usernameInput.setAttribute('check_result', 'success');
            } else {
                alert('다른 아이디를 입력해주세요.');
                usernameInput.setAttribute('check_result', 'fail');
            }
        },
        error: function() {
            alert('오류가 발생했습니다. 다시 시도해주세요.');
            usernameInput.setAttribute('check_result', 'fail');
        }
    });
}

function pushRegiButton(){
	alert("등록되었습니다");
}

function pushResetButton(){
	alert("취소되었습니다");
}