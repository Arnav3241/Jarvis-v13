console.log('CHAT.JS loaded');

const Chat = document.getElementById("msger-chat");

document.getElementById("chatButton").addEventListener("click", function(event){
  event.preventDefault()
  
  input = document.getElementById("msger-input").value;
  document.getElementById("msger-input").value = "";
  console.log(input);
  // document.getElementById("msger-input").disabled = true;

  var d = new Date();

  if (`${d.getMinutes}`.length == 1) { var min = `0${d.getMinutes()}`; } else { var min = d.getMinutes(); }
  if (`${d.getHours()}`.length == 1) { var hr = `0${d.getHours()}`; }    else { var hr = d.getHours(); }

  var z = document.createElement('div');
  z.className = 'msg right-msg';
  z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble"> <div class="msg-info"> <div class="msg-info-name"> Arnav Singh </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${input} </div> </div>`;

  Chat.appendChild(z); 
  Chat.scrollTop = Chat.scrollHeight;
});