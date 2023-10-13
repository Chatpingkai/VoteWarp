// รับ element ใน id="letter"
const letterlist = document.getElementById("wrapper")
const createroom = document.getElementById("createroom")
function addroom(){
    // เพิ่มห้องจดหมาย (img = จดหมาย, text = ชื่อ)
    createroom.remove()
    let img = document.createElement("div")
    img.className = "room_box"
    let text = document.createElement("p")
    text.innerHTML = "แมนซ่า"
    img.appendChild(text)
    letterlist.appendChild(img)
    letterlist.appendChild(createroom)
}