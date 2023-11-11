let profilePic = document.getElementById("profile_smth");
let inputFile = document.getElementById("input-file");
inputFile.onchange = function(){
    profilePic.src = URL.createObjectURL(inputFile.files[0])
}

let profilePics = document.getElementById("background_smth");
let inputFiles = document.getElementById("input-background");
inputFiles.onchange = function(){
    profilePics.src = URL.createObjectURL(inputFiles.files[0])
}

