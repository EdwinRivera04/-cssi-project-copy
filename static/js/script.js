async function getData() {
    let url = `https://picsum.photos/id/${Math.floor((Math.random() * 1084) + 1)}/info`

    let response = await fetch(url);
    let data = await response.json();

    let photo = document.querySelector(".image");
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

    return await data;
}


async function generateLikedPage() {
    let global_data =  await getData();

    let likeButton = document.querySelector("#like")
    let dislikeButton = document.querySelector("#dislike")
    let viewButton = document.querySelector("#view");


    let liked_img = [];
    let disliked_img = [];

<<<<<<< HEAD:static/js/script.js

likeButton.addEventListener("click", () =>{
    getData();
=======
>>>>>>> e46f8660466f0aeeb8ccf7afca69b29db755566d:script.js

    likeButton.addEventListener("click", async () =>{
        liked_img.push(global_data);
        console.log(liked_img)
        // post a new image to screen
        await getData();
    });

    dislikeButton.addEventListener("click", async () =>{
        disliked_img.push(global_data);
        console.log(disliked_img)
        //pot a new image to screen
        await getData();
    });

    viewButton.addEventListener("click",  () => {
        location.href='view.html';
        let liked = document.querySelector(".liked");
        liked.innerHTML = `
        <div>
            <h1>Your Liked images:</h1>
        </div>
        `;
        let disliked = document.querySelector(".disliked");
        disliked.innerHTML = `
        <div>
            <h1>Your disliked images:</h1>
        </div>
        `;
    });
}


generateLikedPage();



