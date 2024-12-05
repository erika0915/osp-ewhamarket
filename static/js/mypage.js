document.addEventListener("DOMContentLoaded", () => {
    const itemsPerPage = 5; // 한 페이지에 보여줄 이미지 수
    const imageList = document.querySelector("#image-List");
    const images = Array.from(imageList.children); // 이미지 노드 리스트
    const paginationContainer = document.querySelector("#pagination-container");

    // 전체 페이지 수 계산
    const totalPages = Math.ceil(images.length / itemsPerPage);

    // 현재 페이지에 따라 이미지를 표시하는 함수
    const displayPage = (page) => {
        // 모든 이미지를 숨기기
        images.forEach((image, index) => {
            image.style.display =
                index >= (page - 1) * itemsPerPage && index < page * itemsPerPage
                    ? "block"
                    : "none";
        });

        // 활성화된 버튼 표시
        Array.from(paginationContainer.children).forEach((btn, idx) => {
            btn.classList.toggle("active", idx + 1 === page);
        });
    };

    // 페이지네이션 버튼 생성
    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement("button");
        button.textContent = i;
        button.addEventListener("click", () => displayPage(i));
        paginationContainer.appendChild(button);
    }

    // 초기화: 첫 페이지를 표시
    if (totalPages > 0) displayPage(1);
});
