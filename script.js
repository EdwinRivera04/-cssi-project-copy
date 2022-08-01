function generateNewCard(text) {
    let imgsrc = 'https://picsum.photos/300'
    let container = document.querySelector(".container");
    container.innerHTML += `
    <div class="row h-100" id="swiping">
        <div class="col d-flex justify-content-center align-items-center h-100">
            <div class="card" style="width: 18rem;">
                <div class="card-body">
                    <img src="${imgsrc}" class="card-img-top" alt="">
                    <p class="card-text">${text}</p>
                </div>
            </div>
        </div>
    </div>`;
}

generateNewCard("hello")


