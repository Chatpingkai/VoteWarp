const check = document.querySelectorAll(".confirm");
check.forEach(ho => {
    ho.addEventListener("click", function() {
        ho.classList.toggle("checked")
    })
})
