const sidepanel = document.querySelector("#mySidepanel");

function openNav() {
    sidepanel.style.width = "300px";
  }

  /* Set the width of the sidebar to 0 (hide it) */
  function closeNav() {
    sidepanel.style.width = "0";
  }