likeButton = document.querySelector("#like")

function likePic(){
    pic = document.querySelector('#current_swipe')
    author_name = pic.alt
    console.log(author_name)
}



likeButton.addEventListener("click", () =>{
    likePic();
});
