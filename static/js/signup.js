function pushRegiButton(){
	alert("등록되었습니다");
}

function pushResetButton(){
	alert("취소되었습니다");
}
/*        <div class="form-row">
            <label class="mkIDc" for="mkId">아이디</label>
            <input type="text" class="username_input" id="mkId" name="userId" placeholder="아이디 입력(6-20자)"> 
            <button type="button" class="id_overlap_button" onclick="id_overlap_check()">ID 중복확인</button>
        </div>
*/

function pushRegiButton(){
    alert("등록되었습니다");
}

function pushResetButton(){
    alert("취소되었습니다");
}

function id_overlap_check() {
    const usernameInput = document.getElementById('mkId');
    const username = usernameInput.value.trim();
    const flashMessageContainer = document.getElementById('flash-messages');
    
    // 입력 검증 함수
    function showMessage(message, type) {
        // Clear previous messages
        flashMessageContainer.innerHTML = '';
        
        // Create new message element
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        messageElement.classList.add('flash-message', type);
        
        // Append to flash message container
        flashMessageContainer.appendChild(messageElement);
        
        // Automatically remove message after 3 seconds
        setTimeout(() => {
            flashMessageContainer.innerHTML = '';
        }, 3000);
    }

    // 입력값 검증
    if (username.length == 0){
        showMessage('아이디를 입력하세요', 'error');
        usernameInput.setAttribute('check_result', 'fail');
        return;
    }

    if (username.length < 6 || username.length > 20) {
        showMessage('아이디는 6-20자 사이여야 합니다.', 'error');
        usernameInput.setAttribute('check_result', 'fail');
        return;
    }

    // Fetch API로 변경 (jQuery 대신)
    fetch('/check_duplicate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.available) {
            showMessage('사용 가능한 아이디입니다.', 'success');
            usernameInput.setAttribute('check_result', 'success');
            usernameInput.classList.add('valid-input');
            usernameInput.classList.remove('invalid-input');
        } else {
            showMessage('다른 아이디를 입력해주세요.', 'error');
            usernameInput.setAttribute('check_result', 'fail');
            usernameInput.classList.add('invalid-input');
            usernameInput.classList.remove('valid-input');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('오류가 발생했습니다. 다시 시도해주세요.', 'error');
        usernameInput.setAttribute('check_result', 'fail');
    });
}