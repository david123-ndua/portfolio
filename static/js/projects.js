/*==================================================
                PROJECTS.JS
        Interactive Portfolio Projects
==================================================*/
document.addEventListener("DOMContentLoaded", () => {

    initProjects();

    initProjectReveal();

});

/*==================================================
                GLOBAL STATE
==================================================*/

let currentFilter = "all";

let currentSearch = "";


/*==================================================
                SCROLL ANIMATION
==================================================*/

function initProjectReveal(){

    const cards=document.querySelectorAll(".project-card");

    const observer=new IntersectionObserver((entries)=>{

        entries.forEach(entry=>{

            if(entry.isIntersecting){

                entry.target.classList.add("show");

                observer.unobserve(entry.target);

            }

        });

    },{

        threshold:.2

    });

    cards.forEach((card,index)=>{

        card.classList.add("hidden");

        card.style.transitionDelay=`${index*120}ms`;

        observer.observe(card);

    });

}



/*==================================================
                EMPTY STATE
==================================================*/

function checkEmptyState(){

    let empty=document.querySelector(".empty-projects");

    const visible=[

        ...document.querySelectorAll(".project-card")

    ].filter(card=>card.style.display!=="none");

    if(visible.length===0){

        if(!empty){

            empty=document.createElement("div");

            empty.className="empty-projects";

            empty.innerHTML=`

                <h2>No projects found</h2>

                <p>Try another keyword or category.</p>

            `;

            document

                .querySelector(".projects-grid")

                .appendChild(empty);

        }

    }

    else{

        if(empty){

            empty.remove();

        }

    }

}

/*==================================================
            INITIALIZE PROJECTS
==================================================*/

function initProjects(){

    const search = document.getElementById("projectSearch");

    const buttons = document.querySelectorAll(".filter-btn");

    if(search){

        search.addEventListener("input",()=>{

            currentSearch = search.value.trim().toLowerCase();

            filterProjects();

        });

    }

    buttons.forEach(button=>{

        button.addEventListener("click",()=>{

            buttons.forEach(btn=>btn.classList.remove("active"));

            button.classList.add("active");

            currentFilter = button.dataset.filter;

            filterProjects();

        });

    });

}

/*==================================================
            FILTER ENGINE
==================================================*/

function filterProjects(){

    const cards = document.querySelectorAll(".project-card");

    cards.forEach(card=>{

        const title = card.querySelector("h3")
            .textContent
            .toLowerCase();

        const description = card.querySelector("p")
            .textContent
            .toLowerCase();

        const categories = card.dataset.category
            .toLowerCase()
            .split(" ");

        const matchesSearch =

            currentSearch === "" ||

            title.includes(currentSearch) ||

            description.includes(currentSearch) ||

            categories.some(category =>
                category === currentSearch
            );

        const matchesFilter =

            currentFilter === "all" ||

            categories.includes(currentFilter);

        if(matchesSearch && matchesFilter){

            card.style.display = "flex";

        }else{

            card.style.display = "none";

        }

    });

    checkEmptyState();

}