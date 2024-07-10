console.log("🚀 eelCode.js loaded");

const Delay = ms => new Promise(res => setTimeout(res, ms));

function JSPrint(text) { 
  console.log("Python " + text); 
}

function myMove() {
  let id = null;
  const elem = document.getElementById("mainCircle");   
  let pos = 0;
  clearInterval(id);
  id = setInterval(frame, 5);
    if (pos == 350) {
      clearInterval(id);
    } else {
      pos++; 
      elem.style.height = pos + "px"; 
      elem.style.width = pos + "px"; 
    }
}
