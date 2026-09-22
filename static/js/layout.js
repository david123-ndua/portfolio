/*==================================================
                LAYOUT.JS
        Global Portfolio Functionality
==================================================*/

document.addEventListener("DOMContentLoaded", () => {

    initMobileMenu();

    initHeader();

});


/*==================================================
                MOBILE MENU
==================================================*/

function initMobileMenu(){

    const menuBtn = document.querySelector(".menu-btn");
    const nav = document.querySelector("nav");

    if(!menuBtn || !nav) return;

    const icon = menuBtn.querySelector("i");

    /* Toggle Mobile Menu */

    menuBtn.addEventListener("click", () => {

        const isOpen = nav.classList.toggle("show");

        icon.classList.toggle("fa-bars", !isOpen);
        icon.classList.toggle("fa-times", isOpen);

        menuBtn.setAttribute("aria-expanded", isOpen);

    });

    /* Close Menu After Clicking a Link */

    document.querySelectorAll("nav a").forEach(link => {

        link.addEventListener("click", () => {

            nav.classList.remove("show");

            icon.classList.remove("fa-times");
            icon.classList.add("fa-bars");

        });

    });

    /* Close Menu When Screen Returns to Desktop */

    window.addEventListener("resize", () => {

        if(window.innerWidth > 768){

            nav.classList.remove("show");

            icon.classList.remove("fa-times");
            icon.classList.add("fa-bars");

        }

    });

}


/*==================================================
            HEADER SCROLL EFFECT
==================================================*/

function initHeader(){

    const header = document.querySelector("header");

    if(!header) return;

    window.addEventListener("scroll", () => {

        if(window.scrollY > 40){

            header.classList.add("scrolled");

        }

        else{

            header.classList.remove("scrolled");

        }

    });

}