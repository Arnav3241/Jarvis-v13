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

// Demo History
// [{'Data': 'Hello', 'Date': '12/12/2021'}, {'Data': 'Hello', 'Date': '12/12/2021'}, {'Data': 'hello Howe are you', 'Date': '2024-07-21T09:36:29.001Z'}, {'Data': 'Yes it is working', 'Date': '2024-07-21T09:36:38.249Z'}, {'Data': 'Hello', 'Date': '2024-07-21T09:37:40.702Z'}, {'Data': 'Hello', 'Date': '2024-07-21T09:39:00.622Z'}]

ChatHistory = []

eel.RestoreHistory("1")((data) => {
  ChatHistory = data;
  console.log(data);
  for (var i = 0; i < data.length; i++) {
    var d = new Date(data[i]["Date"]);
    if (`${d.getMinutes}`.length == 1) { var min = `0${d.getMinutes()}`; } else { var min = d.getMinutes(); }
    if (`${d.getHours()}`.length == 1) { var hr = `0${d.getHours()}`; }    else { var hr = d.getHours(); }

    if (data[i]["Role"] == "user") {
      var z = document.createElement('div');
      z.className = 'msg right-msg';
      z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble"> <div class="msg-info"> <div class="msg-info-name"> Arnav Singh </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${data[i]["Data"]} </div> </div>`;
      Chat.appendChild(z);
    }
    else {
      var z = document.createElement('div');
      z.className = 'msg left-msg';
      z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble"> <div class="msg-info"> <div class="msg-info-name"> Jarvis </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${data[i]["Data"]} </div> </div>`;
      Chat.appendChild(z);
    }
  }
  Chat.scrollTop = Chat.scrollHeight;
});
