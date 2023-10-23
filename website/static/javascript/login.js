function cloud_transition() {
    const cloudimation = document.getElementById("cloudimation");
    cloudimation.style.display = "block";
    cloudimation.style.animation = "cloud 3s";
}
setTimeout(function() {
    var cloudImage = document.querySelector(".cloudimation");
    cloudImage.style.display = "none"; // ซ่อนรูปภาพหลังจาก 3 วินาที
}, 3000);