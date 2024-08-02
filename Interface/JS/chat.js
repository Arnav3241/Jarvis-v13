console.log('CHAT.JS loaded');

const Chat = document.getElementById("msger-chat");

document.getElementById("chatButton").addEventListener("click", function(event){
  event.preventDefault()
  
  input = document.getElementById("msger-input").value;
  document.getElementById("msger-input").value = "";
  console.log(input);
    // document.getElementById("msger-input").disabled = true;
  if (input == "") { return; }
  var d = new Date();

  if (`${d.getMinutes}`.length == 1) { var min = `0${d.getMinutes()}`; } else { var min = d.getMinutes(); }
  if (`${d.getHours()}`.length == 1) { var hr = `0${d.getHours()}`; }    else { var hr = d.getHours(); }

  var z = document.createElement('div');
  z.className = 'msg right-msg';
  z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble"> <div class="msg-info"> <div class="msg-info-name"> Arnav Singh </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${input} </div> </div>`;

  Chat.appendChild(z); 
  Chat.scrollTop = Chat.scrollHeight;

  eel.AddToUserHistory(input, d, "1", "user");
});

ChatHistory = []

eel.expose(funcUpdateChat);
function funcUpdateChat(data) {
  console.log(data);
  var d = new Date(data["Date"]);
  if (`${d.getMinutes}`.length == 1) { var min = `0${d.getMinutes()}`; } else { var min = d.getMinutes(); }
  if (`${d.getHours()}`.length == 1) { var hr = `0${d.getHours()}`; }    else { var hr = d.getHours(); }

  if (data["Role"] == "user") {
    var z = document.createElement('div');
    z.className = 'msg right-msg';
    z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble"> <div class="msg-info"> <div class="msg-info-name"> Arnav Singh </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${data["Data"]} </div> </div>`;
    Chat.appendChild(z);
  }
  else {
    var z = document.createElement('div');
    z.className = 'msg left-msg';
    z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble "> <div class="msg-info"> <div class="msg-info-name"> Jarvis </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${data["Data"]} </div> </div>`;
    Chat.appendChild(z);
  }
  Chat.scrollTop = Chat.scrollHeight;
}


eel.RestoreHistory("1")((data) => {
  ChatHistory = data;
  console.log(data);
  for (var i = 0; i < data.length; i++) {
    funcUpdateChat(data[i]);
  }
  Chat.scrollTop = Chat.scrollHeight;
});

function funcUpdateChatFromPy() {
  eel.RestoreHistory("1")((data) => {
    ChatHistory = data;
    console.log(data);
    for (var i = 0; i < data.length; i++) {
      funcUpdateChat(data[i]);
    }
    Chat.scrollTop = Chat.scrollHeight;
  });
}
