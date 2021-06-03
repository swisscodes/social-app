const burgerButton = document.querySelector(".burger-button");
const linkMenu = document.querySelector(".link-menu");

burgerButton.onclick = () => {
    burgerButton.classList.toggle("is-active");
    linkMenu.classList.toggle("drop-it");
};

// const burgerButton = document.querySelector(".burger-button");

// burgerButton.addEventListener("click", function () {
//     this.classList.toggle("is-active");
// });
