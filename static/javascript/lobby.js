// รับ element ใน id="letter"
const letterlist = document.getElementById("letter")
function addroom(){
    // เพิ่มห้องจดหมาย (img = จดหมาย, text = ชื่อ)
    let img = document.createElement("img")
    img.src = "../static/img/letter.png"
    let text = document.createElement("div")
    text.innerHTML = "Name"
    letterlist.appendChild(img)
    letterlist.appendChild(text)
}
