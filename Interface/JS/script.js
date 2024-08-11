console.log("🚀 eelCode.js loaded");
const dropdownButton = document.querySelector('.dropdown button');

var currentSoul = "";
var currentSoul_name = "";

eel.getSoul()((soul) => {
  currentSoul = soul;
  if ("Jarvis" == soul) { currentSoul_name = "Jarvis (Default AI)"; }
  if ("Kakashi_Hatake" == soul) { currentSoul_name = "Kakashi Hatake"; }
  if ("Light_Yagami" == soul) { currentSoul_name = "Light Yagami"; }
  if ("Senku_Ishigami" == soul) { currentSoul_name = "Senku Ishigami"; }
  if ("Hinata_Hyuga" == soul) { currentSoul_name = "Hinata Hyuga"; }
  if ("Yui_Hirasawa" == soul) { currentSoul_name = "Yui Hirasawa"; }
  if ("Failed_Genious_AI" == soul) { currentSoul_name = "Failed Genius AI"; }

  dropdownButton.innerHTML = currentSoul_name;
})


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

eel.expose(changeSoul);
function changeSoul(soul) {
  currentSoul = soul;
  if ("Jarvis" == soul) { currentSoul_name = "Jarvis (Default AI)"; }
  if ("Kakashi_Hatake" == soul) { currentSoul_name = "Kakashi Hatake"; }
  if ("Light_Yagami" == soul) { currentSoul_name = "Light Yagami"; }
  if ("Senku_Ishigami" == soul) { currentSoul_name = "Senku Ishigami"; }
  if ("Hinata_Hyuga" == soul) { currentSoul_name = "Hinata Hyuga"; }
  if ("Yui_Hirasawa" == soul) { currentSoul_name = "Yui Hirasawa"; }
  if ("Failed_Genious_AI" == soul) { currentSoul_name = "Failed Genius AI"; }

  eel.RestoreHistory(currentSoul);
  dropdownButton.innerHTML = currentSoul_name;
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
  eel.JSprint("Terminating...");
  window.close();
});

eel.expose(close_window)
function close_window() {
    window.close()
}