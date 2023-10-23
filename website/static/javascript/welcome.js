let vid = document.getElementById("planevideo")
function playvid() {
    vid.play()
}

function cloud_transition_login() {
    const cloudimation = document.getElementById("cloudimation");
    cloudimation.style.display = "block";
    cloudimation.style.animation = "cloud 3s";
    setTimeout(wait_login, 2500)
}
function wait_login() {
    window.location.href = "login.html";
}
function cloud_transition_register() {
    const cloudimation = document.getElementById("cloudimation");
    cloudimation.style.display = "block";
    cloudimation.style.animation = "cloud 3s";
    setTimeout(wait_register, 2500)
}
function wait_register() {
    window.location.href = "Register.html";
}