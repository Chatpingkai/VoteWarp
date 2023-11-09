const check = document.querySelectorAll(".confirm");
check.forEach(ho => {
    ho.addEventListener("click", function() {
        ho.classList.toggle("checked")
    })
})

function openchat(){
    var chatroom = document.querySelector(".chatroom");
    chatroom.style.display = "block";
    chatroom.style.animation = "popup 1.5s"
}

function closechat(){
    var chatroom = document.querySelector(".chatroom");
    chatroom.style.animation = "popdown 1.5s"
    setTimeout(hehe, 1500)
}

function hehe(){
    var chatroom = document.querySelector(".chatroom");
    chatroom.style.display = "none";
}
