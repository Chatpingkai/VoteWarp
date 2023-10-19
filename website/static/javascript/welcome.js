let vid = document.getElementById("planevideo")
function playvid() {
    vid.play()
}

function cloud_transition() {
    const cloudimation = document.getElementById("cloudimation");
    cloudimation.style.display = "block";
    cloudimation.style.animation = "cloud 3s";
    setTimeout(waitnewpage, 3000)
}
function waitnewpage() {
    window.location.href = "login.html";
}