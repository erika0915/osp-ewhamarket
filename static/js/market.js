function showHeart() {
    $.ajax({
    type: 'GET',
    url: '/likes/show_heart/{{name}}/',
    data: {},
    success: function (response) {
    let my_heart = response['my_heart'];
    if (my_heart['interested'] == 'Y')
    {
    $("#heart").css("color","red");
    $("#heart").attr("onclick","unlike()");
    }
    else
    {
    $("#heart").css("color","grey");
    $("#heart").attr("onclick","like()");
    }
    //alert("showheart!")
    }
    });
}

function like() {
    $.ajax({
    type: 'POST',
    url: '/likes/like/{{name}}/',
    data: {
    interested : "Y"
    },
    success: function (response) {
    alert(response['msg']);
    window.location.reload()
    }
    });
}

function unlike() {
    $.ajax({
    type: 'POST',
    url: '/likes/unlike/{{name}}/',
    data: {
    interested : "N"
    },
    success: function (response) {
    alert(response['msg']);
    window.location.reload()
    }
    });
}

$(document).ready(function () {
    showHeart();
});

$(document).ready(function () { 
    $('#category option:conatins("{{category")').prop("selected",true);
});


// 페이지네이션 함수
function changePage(nickname, direction) {
    const listContainer = document.getElementById(`sellList-${nickname}`);
    const items = Array.from(listContainer.querySelectorAll('.image-wrapper'));
    const totalItems = items.length;
    const itemsPerPage = 5; // 한 페이지당 표시할 상품 수
    const totalPages = Math.ceil(totalItems / itemsPerPage);
  
    // 현재 페이지 찾기
    let currentPage = parseInt(listContainer.dataset.currentPage || "0", 10);
  
    // 새 페이지 계산
    const newPage = currentPage + direction;
    if (newPage < 0 || newPage >= totalPages) return; // 경계 초과 방지
  
    // 업데이트된 현재 페이지 저장
    listContainer.dataset.currentPage = newPage;
  
    // 상품 표시 업데이트
    items.forEach((item, index) => {
      const itemPage = Math.floor(index / itemsPerPage);
      item.style.display = itemPage === newPage ? "block" : "none";
    });
  
    // 버튼 상태 업데이트
    const prevButton = listContainer.parentNode.querySelector('.prev-button');
    const nextButton = listContainer.parentNode.querySelector('.next-button');
    prevButton.disabled = newPage === 0;
    nextButton.disabled = newPage === totalPages - 1;
  }
  
  // 초기화 함수
  function initializePagination() {
    const lists = document.querySelectorAll('.image-List');
    lists.forEach((list) => {
      const items = Array.from(list.querySelectorAll('.image-wrapper'));
      const itemsPerPage = 5;
      const totalPages = Math.ceil(items.length / itemsPerPage);
  
      // 초기 페이지 설정
      list.dataset.currentPage = 0;
  
      // 상품 숨기고 첫 페이지 상품만 표시
      items.forEach((item, index) => {
        const itemPage = Math.floor(index / itemsPerPage);
        item.style.display = itemPage === 0 ? "block" : "none";
      });
  
      // 버튼 초기화
      const prevButton = list.parentNode.querySelector('.prev-button');
      const nextButton = list.parentNode.querySelector('.next-button');
      prevButton.disabled = true;
      nextButton.disabled = totalPages <= 1;
    });
  }
  
  // 페이지 로드 시 초기화
  document.addEventListener('DOMContentLoaded', initializePagination);
  