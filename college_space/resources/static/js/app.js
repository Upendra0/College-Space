const sidepanel = document.querySelector("#mySidepanel");

function openNav() {
  sidepanel.style.width = "350px";
}

/* Set the width of the sidebar to 0 (hide it) */
function closeNav() {
  sidepanel.style.width = "0";
};

var loadFile = function (event) {
  var image = document.getElementById("output");
  image.src = URL.createObjectURL(event.target.files[0]);
};