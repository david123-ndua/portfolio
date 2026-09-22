/*==========================================
    HOME PAGE
==========================================*/

const words = [

    "Java Developer",

    "Flask Developer",

    "Full Stack Developer",

    "MERN Stack Developer",

    "Backend Developer"

];

const typingText = document.getElementById("typing-text");

let wordIndex = 0;

let charIndex = 0;

let deleting = false;

function typeEffect(){

    if(!typingText) return;

    const currentWord = words[wordIndex];

    if(!deleting){

        typingText.textContent = currentWord.substring(0, charIndex + 1);

        charIndex++;

        if(charIndex === currentWord.length){

            deleting = true;

            setTimeout(typeEffect, 1800);

            return;

        }

    }else{

        typingText.textContent = currentWord.substring(0, charIndex - 1);

        charIndex--;

        if(charIndex === 0){

            deleting = false;

            wordIndex++;

            if(wordIndex >= words.length){

                wordIndex = 0;

            }

        }

    }

    const speed = deleting ? 45 : 90;

    setTimeout(typeEffect, speed);

}

window.addEventListener("load", () => {

    typeEffect();

});