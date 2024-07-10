const body = document.querySelector('body'), sidebar = body.querySelector('nav'), toggle = body.querySelector(".toggle");

sidebar.classList.toggle("close");

toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
})

searchBtn.addEventListener("click", () => {
  sidebar.classList.remove("close");
})
