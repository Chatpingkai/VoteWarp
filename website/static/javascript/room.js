let check = document.querySelectorAll(".confirm");
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
    setTimeout(delay_closechat, 1000)
}

function delay_closechat(){
    var chatroom = document.querySelector(".chatroom");
    chatroom.style.display = "none";
}

function openvote(){
    console.log("he")
    var createvote = document.querySelector(".create_vote");
    createvote.style.display = "flex";
    createvote.style.animation = "invote 1s"
}

function closevote(){
    var createvote = document.querySelector(".create_vote");
    createvote.style.animation = "outvote 1s"
    setTimeout(delay_close, 1000)
}

function delay_close(){
    var createvote = document.querySelector(".create_vote");
    createvote.style.display = "none";
}

function createvote(){
    const votecontainer = document.getElementById("voting");
    console.log("yOOO");
    console.log(votecontainer)
    let votingbox = document.createElement("div");
    votingbox.className = "votingbox";
    let picture = document.createElement("div");
    picture.className = "picture";
    let class_place = document.createElement("div");
    class_place.className = "place";
    let text_place = document.createElement("p");
    text_place.innerHTML = "place:";
    let line2_place = document.createElement("div");
    line2_place.className = "line2";
    let text_place_input = document.createElement("p");
    text_place_input.innerHTML = "ร้านเหล้าแถวนี้";
    line2_place.appendChild(text_place_input);
    class_place.appendChild(text_place);
    class_place.appendChild(line2_place);

    let whitebox = document.createElement("div");
    whitebox.className = "whitebox";
    let class_date = document.createElement("div");
    class_date.className = "date";
    let text_date = document.createElement("p");
    text_date.innerHTML = "date:";
    let line2_date = document.createElement("div");
    line2_date.className = "line2";
    let text_date_input = document.createElement("p");
    text_date_input.innerHTML = "07/10/2023";
    line2_date.appendChild(text_date_input);
    class_date.appendChild(text_date);
    class_date.appendChild(line2_date);

    let class_timey = document.createElement("div");
    class_timey.className = "timey";
    let text_timey = document.createElement("p");
    text_timey.innerHTML = "time:";
    let line2_time = document.createElement("div");
    line2_time.className = "line2";
    let text_time_input = document.createElement("p");
    text_time_input.innerHTML = "22.00 น.";
    line2_time.appendChild(text_time_input);
    class_timey.appendChild(text_timey);
    class_timey.appendChild(line2_time);

    let votingtext = document.createElement("div");
    votingtext.className = "votingtext";
    let voting_p = document.createElement("p");
    voting_p.innerHTML = "voting";
    let user_votingbox = document.createElement("div");
    user_votingbox.className = "user_votingbox";
    let user_voting = document.createElement("div");
    user_voting.className = "user_voting";
    user_votingbox.appendChild(user_voting.cloneNode(true));
    user_votingbox.appendChild(user_voting.cloneNode(true));
    user_votingbox.appendChild(user_voting.cloneNode(true));
    votingtext.appendChild(voting_p);
    votingtext.appendChild(user_votingbox);

    let confirm = document.createElement("div");
    confirm.className = "confirm";
    
    whitebox.appendChild(class_date);
    whitebox.appendChild(class_timey);
    whitebox.appendChild(votingtext);
    whitebox.appendChild(confirm);

    votingbox.appendChild(picture);
    votingbox.appendChild(class_place);
    votingbox.appendChild(whitebox);
    votecontainer.appendChild(votingbox)
    check = document.querySelectorAll(".confirm")
    check.forEach(ho => {
        ho.addEventListener("click", function() {
            ho.classList.toggle("checked")
        })
    })
    console.log(check)
    closevote();
}


let profilePicture = document.getElementById("picture_room");
let inputfile = document.getElementById("input-file");
inputfile.onchange = function(){
    profilePicture.src = URL.createObjectURL(inputfile.files[0])
}
