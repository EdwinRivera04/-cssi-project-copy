
import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.9.1/firebase-app.js'

// If you enabled Analytics in your project, add the Firebase SDK for Google Analytics

// Add Firebase products that you want to use
import { auth } from 'https://www.gstatic.com/firebasejs/9.9.1/firebase-auth.js'
import { firestore } from 'https://www.gstatic.com/firebasejs/9.9.1/firebase-firestore.js'


const firebaseConfig = {
    apiKey: "AIzaSyDsa0s1k86mV8liwsYDJo4_OTBZlwC06ac",
    authDomain: "cssi-final-project-6d1b6.firebaseapp.com",
    projectId: "cssi-final-project-6d1b6",
    storageBucket: "cssi-final-project-6d1b6.appspot.com",
    messagingSenderId: "645672514669",
    appId: "1:645672514669:web:f4e5491222e8eb0ab17b64",
    measurementId: "G-CM4SCS7HE4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

let signin_button = document.querySelector('#signin');

signin_button.addEventListener('click', () =>{
    const GoogleAuth = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithPopup(googleAuth);
});
export default Firebase;
