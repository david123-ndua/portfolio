/*==================================================
                CONTACT.JS
        Contact Page Functionality
==================================================*/

document.addEventListener("DOMContentLoaded", () => {

    initContactReveal();

});


/*==================================================
            SCROLL REVEAL
==================================================*/

function initContactReveal(){

    const elements = document.querySelectorAll(

        ".contact-card, .contact-form-card"

    );

    const observer = new IntersectionObserver((entries)=>{

        entries.forEach(entry=>{

            if(entry.isIntersecting){

                entry.target.classList.add("show");

                observer.unobserve(entry.target);

            }

        });

    },{

        threshold:0.2

    });

    elements.forEach((element,index)=>{

        element.classList.add("hidden");

        element.style.transitionDelay = `${index * 120}ms`;

        observer.observe(element);

    });

}


/*==================================================
            CONTACT FORM
==================================================*/
function initContactForm(){

    const form = document.getElementById("contactForm");

    if(!form) return;

    form.addEventListener("submit", function(e){

        const email = document
            .getElementById("email")
            .value
            .trim();

        if(!validateEmail(email)){

            e.preventDefault();

            showMessage(
                "Please enter a valid email address.",
                false
            );

            return;
        }

        const button = form.querySelector("button");

        button.disabled = true;

        button.innerHTML =
            '<i class="fas fa-spinner fa-spin"></i> Sending...';

    });

}

/*==================================================
            EMAIL VALIDATION
==================================================*/

function validateEmail(email){

    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

}


/*==================================================
            SUCCESS / ERROR MESSAGE
==================================================*/

function showMessage(message, success){

    let box = document.querySelector(".contact-message");

    if(!box){

        box = document.createElement("div");

        box.className = "contact-message";

        document

            .querySelector(".contact-form-card")

            .prepend(box);

    }

    box.textContent = message;

    box.classList.remove(

        "success",

        "error"

    );

    box.classList.add(

        success ? "success" : "error"

    );

    box.style.display = "block";

    setTimeout(()=>{

        box.style.display = "none";

    },4000);

}