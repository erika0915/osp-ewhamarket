<script>
document.addEventListener('DOMContentLoaded', () => {
    const products = Array.from(document.querySelectorAll('.product')); // 모든 상품 요소
    const itemsPerPage = 6; // 페이지당 표시할 상품 개수
    const pagination = document.querySelector('.pagination');
    const pageNumbers = pagination.querySelector('.page-numbers');
    const prevButton = pagination.querySelector('.prev-page');
    const nextButton = pagination.querySelector('.next-page');
    let currentPage = 1;

    // 전체 페이지 수 계산
    const totalPages = Math.ceil(products.length / itemsPerPage);

    // 페이지 버튼 생성
    function renderPagination() {
        pageNumbers.innerHTML = ''; // 초기화
        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement('button');
            button.textContent = i;
            button.classList.add('page-button');
            if (i === currentPage) button.classList.add('active');
            button.addEventListener('click', () => {
                currentPage = i;
                updateDisplay();
            });
            pageNumbers.appendChild(button);
        }
    }

    // 상품 표시 업데이트
    function updateDisplay() {
        // 모든 상품 숨기기
        products.forEach(product => (product.style.display = 'none'));

        // 현재 페이지의 상품만 표시
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        products.slice(start, end).forEach(product => (product.style.display = 'flex'));

        // 버튼 활성화/비활성화
        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;

        // 페이지 버튼 활성화 상태 업데이트
        renderPagination();
    }

    // 이전 버튼 클릭
    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            updateDisplay();
        }
    });

    // 다음 버튼 클릭
    nextButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            updateDisplay();
        }
    });

    // 초기 표시
    updateDisplay();
});

let demo = document.getElementById("demo");

// demo 부분에 클릭 이벤트
demo.addEventListener("click", function() {
  demo.classList.toggle('click');
}) 

</script>
