const email = document.querySelector("#email");
const password = document.querySelector("#password")

console.log(email.value);
console.log(password.value);


const logInButton = document.querySelector("#lN");

logInButton.addEventListener("click", () => {
    if(email.value.toLowerCase() === "alice@gmail.com" && password.value.toLowerCase() === "googlecssi"){
    location.href="top.html";
   }
  else
    alert("Wrong Email and/or Password");
});