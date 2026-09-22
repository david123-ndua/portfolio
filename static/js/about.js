/*==================================================
                ABOUT PAGE
==================================================*/

document.addEventListener("DOMContentLoaded", () => {

    initScrollReveal();

    initTimelineAnimation();

    initCardAnimation();

});


/*==================================================
                SCROLL REVEAL
==================================================*/

function initScrollReveal() {

    const elements = document.querySelectorAll(

        ".fade-left, .fade-right, .education-card, .expertise-card, .build-card, .cta-box"

    );

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

                observer.unobserve(entry.target);

            }

        });

    }, {

        threshold: 0.20

    });

    elements.forEach(element => {

        element.classList.add("hidden");

        observer.observe(element);

    });

}


/*==================================================
            TIMELINE ANIMATION
==================================================*/

function initTimelineAnimation() {

    const timelineItems = document.querySelectorAll(".timeline-item");

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("timeline-show");

                observer.unobserve(entry.target);

            }

        });

    }, {

        threshold: 0.35

    });

    timelineItems.forEach(item => {

        item.classList.add("timeline-hidden");

        observer.observe(item);

    });

}


/*==================================================
            STAGGERED CARD ANIMATION
==================================================*/

function initCardAnimation() {

    const cards = document.querySelectorAll(

        ".education-card, .expertise-card, .build-card"

    );

    cards.forEach((card, index) => {

        card.style.transitionDelay = `${index * 120}ms`;

    });

}