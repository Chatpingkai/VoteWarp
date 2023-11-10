
function popup_createroom(){
    document.querySelector(".popup_box").style.display = "flex";
}
function close_popup() {
    var popupBox = document.querySelector(".popup_box");
    popupBox.style.display = "none";

    // หาทุกอินพุตในกล่องข้อความ
    var inputFields = popupBox.querySelectorAll("input, textarea");

    // เคลียข้อความในทุกอินพุตที่ไม่ใช่ "submit"
    inputFields.forEach(function (inputField) {
        if (inputField.type !== "submit") {
            inputField.value = "";
        }
    });
}
// เพิ่ม room_box
const box = document.getElementById("wrapper");
const createroom = document.getElementById("createroom");
const statuslist = ["room_box green", "room_box yellow"]
function addroom(){
    // เพิ่มห้องจดหมาย (img = จดหมาย, text = ชื่อ)
    createroom.remove();
    let room_box = document.createElement("div");
    room_box.className = statuslist[Math.floor(Math.random()*statuslist.length)];
    let text_room = document.createElement("p");
    let name_room = document.createElement("p");
    let text_status = document.createElement("p");
    let complete = document.createElement("p");
    let text_place = document.createElement("p");
    let text_date = document.createElement("p");
    let text_time = document.createElement("p");
    text_room.innerHTML = "room"
    name_room.innerHTML = document.getElementById("groupname").value;
    text_status.innerHTML = "status:"
    if (room_box.className === "room_box green") {
        complete.innerHTML = "complete"
    } else {
        complete.innerHTML = "voting"
    }
    text_place.innerHTML = "place:"
    text_place.className = "text_place"
    text_date.innerHTML = "date:"
    text_date.className = "text_date"
    text_time.innerHTML = "time:"
    text_time.className = "text_time"
    let line_place = document.createElement("p");
    let line_date = document.createElement("p");
    let line_time = document.createElement("p");
    line_place.innerHTML = "ร้านเหล้าแถวนี้"
    line_date.innerHTML = document.getElementById("selectedDate").value;
    line_time.innerHTML = "22.00 น."
    let line = document.createElement("div");
    line.className = "line"
    let status = document.createElement("div");
    status.className = "status"
    let place = document.createElement("div");
    place.className = "place"
    let date = document.createElement("div");
    date.className = "date"
    let timey = document.createElement("div");
    timey.className = "timey"
    let picpic = document.createElement("div");
    picpic.className = "picpic"
    picpic.setAttribute("id", "picpic")
    picpic.style.backgroundImage = "url("+profilePicture.src+")"
    let line_1 = document.createElement("div");
    line_1.className = "line2"
    let line_2 = document.createElement("div");
    line_2.className = "line2"
    let line_3 = document.createElement("div");
    line_3.className = "line2"
    // line_1.appendChild(line_place);
    line_2.appendChild(line_date);
    // line_3.appendChild(line_time);
    let check_img = document.createElement("img");
    if (room_box.className === "room_box green") {
        check_img.src = "../static/img/check-mark (1).png"
    } else {
        check_img.src = "../static/img/voteting.png"
    }
    line.appendChild(name_room)
    status.appendChild(text_status)
    status.appendChild(complete)
    status.appendChild(check_img)
    // place.appendChild(text_place)
    // place.appendChild(line_1)
    date.appendChild(text_date)
    date.appendChild(line_2)
    // timey.appendChild(text_time)
    // timey.appendChild(line_3)
    room_box.appendChild(text_room)
    room_box.appendChild(line)
    room_box.appendChild(status)
    room_box.appendChild(place)
    room_box.appendChild(date)
    room_box.appendChild(timey)
    room_box.appendChild(picpic)
    box.appendChild(room_box)
    box.appendChild(createroom)
    close_popup()
}
// ทำให้ room_box ขยับซ้ายขวาได้
const tabBox = document.querySelector(".wrapper");

let isDragging = false;

const dragging = (e) => {
    if(!isDragging) return;
    tabBox.scrollLeft -= e.movementX;
}

const dragstop = () => {
    isDragging = false;
}

tabBox.addEventListener("mousedown", () => isDragging = true);
tabBox.addEventListener("mousemove", dragging);
document.addEventListener("mouseup", dragstop);

// const getFontSize = (textLength) => {
//     const baseSize = 20
//     if (textLength >= baseSize) {
//       textLength = baseSize - 2
//     }
//     const fontSize = baseSize - textLength
//     return `${fontSize}vw`
//   }
  
//   const boxes = document.querySelectorAll('.name_user p')
    
//   boxes.forEach(box => {
//     box.style.fontSize = getFontSize(box.textContent.length)
//   })

let profilePicture = document.getElementById("picture_room");
let inputfile = document.getElementById("input-file");
inputfile.onchange = function(){
    profilePicture.src = URL.createObjectURL(inputfile.files[0])
}
