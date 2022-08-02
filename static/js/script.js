async function getData() {
    let url = `https://picsum.photos/id/${Math.floor((Math.random() * 1084) + 1)}/info`

    let response = await fetch(url);
    let data = await response.json();

    let photo = document.querySelector(".container");
    photo.innerHTML = `
    <div class="row h-100" id="swiping">
        <div class="col d-flex justify-content-center align-items-center h-100">
            <div class="card" style="width: 18rem;">
                <div class="card-body">
                    <img src="${data.download_url}" class="card-img-top" alt="${data.author}'s image">
                    <p class="card-text">${data.author}'s image</p>
                </div>
            </div>
        </div>
    </div>`;
}

getData();

let likeButton = document.querySelector("#like")
let dislikeButton = document.querySelector("#dislike")


likeButton.addEventListener("click", () =>{
    getData();

});

dislikeButton.addEventListener("click", () =>{
    getData();

});

