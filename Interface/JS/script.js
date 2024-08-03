console.log("🚀 eelCode.js loaded");

document.documentElement.webkitRequestFullscreen();

const Delay = ms => new Promise(res => setTimeout(res, ms));
document.addEventListener('contextmenu', event => event.preventDefault());

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

window.onload = function() {
  eel.RefreshGlobalVars()((data) => {
    GlobalVars = data;
    console.log(data);
  })
}

document.getElementById("ExitBtn").addEventListener("click", function(event){
  event.preventDefault()
  eel.Terminate();
  eel.PPPrint("Terminating...");
  window.close();
});

eel.expose(close_window)
function close_window() {
    window.close()
}