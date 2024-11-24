/*김연우*/
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>

function setThumbnail(event) {
    var reader = new FileReader();
    reader.onload = function(event) {
        var img = document.createElement("img");
        img.setAttribute("src", event.target.result);

        img.style.maxWidth = "300px";

        var container = document.querySelector("div#image_container");
        container.innerHTML = ''; // 기존 이미지 제거
        container.appendChild(img);
    };
    reader.readAsDataURL(event.target.files[0]);
}

$(document).ready(function() {
    $('.star_rating > .star').click(function() {
        var value = $(this).attr('value'); // 선택된 별점 값
        $(this).parent().children('.star').removeClass('on');
        $(this).addClass('on').prevAll('.star').addClass('on');
        console.log('선택된 별점:', value); // 선택된 별점 값 확인
    });


    $('.file').change(function() {
        var fileName = $(this).val().split('\\').pop();
        $(this).prev('.file-label').text(fileName || 'choose file');
    });
});


function pushRegiButton(){
    alert("등록되었습니다")
}