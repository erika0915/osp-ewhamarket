// 별점 숫자 (서버에서 가져온 값으로 변경 가능)
const starRating = parseInt("{{ review.rate }}");

console.log(starRating);
 
// 별점 생성 함수
function generateStars(rating) {
    const starContainer = document.getElementById("star-rating");
    starContainer.innerHTML = ""; // 기존 내용을 초기화
    
    for (let i = 0; i < 5; i++) {
        const star = document.createElement("span");
        if (i < rating) {
            star.textContent = "★"; // 채워진 별
            star.style.color = "#FFD700"; 
        } else {
            star.textContent = "☆"; // 빈 별
            star.style.color = "#ddd"; 
        }
        star.style.fontSize = "20px";
        star.style.marginRight = "5px";
        starContainer.appendChild(star);
    }
}
    
// 별점 적용
generateStars(starRating);