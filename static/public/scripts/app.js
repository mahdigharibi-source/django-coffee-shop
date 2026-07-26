const toggleThemeBtn = document.querySelectorAll("#toggle-theme");
const submenuOpenBtn = document.querySelector(".submenu-open-btn")
const submenu = document.querySelector(".submenu")
const navOpenBtn = document.querySelector(".nav-icon")
const navItem = document.querySelector(".nav")
const overlay = document.querySelector(".overlay")
const closeBtn = document.querySelector(".close-btn")
const cartIcon = document.querySelector(".cart-icon")
const cartCloseBtn = document.querySelector(".cart-close-btn")
const cart = document.querySelector(".cart")


toggleThemeBtn.forEach(btn => {
    btn.addEventListener("click", function () {
        if (localStorage.theme === "dark") {
            document.documentElement.classList.remove("dark");
            localStorage.theme = "light";
        } else {
            document.documentElement.classList.add("dark");
            localStorage.setItem("theme", "dark");
        }
    })
})


submenuOpenBtn.addEventListener("click", (e) => {
    e.currentTarget.parentElement.classList.toggle("text-orange-300")
    submenu.classList.toggle('submenu--open')
})

navOpenBtn.addEventListener("click", () => {

    navItem.classList.remove("-right-64")
    navItem.classList.add("right-0")
    overlay.classList.remove("hidden")
    overlay.classList.add("flex")

})


closeBtn.addEventListener("click", () => {
    navItem.classList.remove("right-0")
    navItem.classList.add("-right-64")
    overlay.classList.remove("flex")
    overlay.classList.add("hidden")

})

cartIcon.addEventListener("click", () => {
    cart.classList.remove("-left-64")
    cart.classList.add("left-0")
})

cartCloseBtn.addEventListener("click", ()=>{
    cart.classList.remove("left-0")
    cart.classList.add("-left-64")
})












// toggleThemeBtn.addEventListener("click" , () => {
//     if (localStorage.theme === "dark"){
//         document.documentElement.classList.remove("dark");
//         localStorage.theme = "light";
//     } else {
//         document.documentElement.classList.add("dark");
//         localStorage.setItem("theme" , "dark");
//     }
// })