// console.log('CHAT.JS loaded');

const Chat = document.getElementById("msger-chat");

document.getElementById("chatButton").addEventListener("click", function (event) {
  event.preventDefault()

  input = document.getElementById("msger-input").value;
  document.getElementById("msger-input").value = "";
  // console.log(input);
  // document.getElementById("msger-input").disabled = true;
  if (input == "") { return; }
  var d = new Date();

  if (`${d.getMinutes}`.length == 1) { var min = `0${d.getMinutes()}`; } else { var min = d.getMinutes(); }
  if (`${d.getHours()}`.length == 1) { var hr = `0${d.getHours()}`; } else { var hr = d.getHours(); }

  var z = document.createElement('div');
  z.className = 'msg right-msg';
  z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble"> <div class="msg-info"> <div class="msg-info-name"> Arnav Singh </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${input} </div> </div>`;

  Chat.appendChild(z);
  Chat.scrollTop = Chat.scrollHeight;

  eel.AddToUserHistory(input, d, "1");
});

ChatHistory = []

// eel.expose(funcUpdateChat);
// function funcUpdateChat(data) {
//   // console.log(data);
//   var d = new Date(data["Date"]);
//   if (`${d.getMinutes}`.length == 1) { var min = `0${d.getMinutes()}`; } else { var min = d.getMinutes(); }
//   if (`${d.getHours()}`.length == 1) { var hr = `0${d.getHours()}`; } else { var hr = d.getHours(); }

//   if (data["Role"] == "user") {
//     var z = document.createElement('div');
//     z.className = 'msg right-msg';
//     z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble"> <div class="msg-info"> <div class="msg-info-name"> Arnav Singh </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${data["Data"]} </div> </div>`;
//     Chat.appendChild(z);
//   }
//   else {
//     var z = document.createElement('div');
//     z.className = 'msg left-msg';
//     z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble "> <div class="msg-info"> <div class="msg-info-name"> Jarvis </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${data["Data"]} </div> </div>`;
//     Chat.appendChild(z);
//   }
//   Chat.scrollTop = Chat.scrollHeight;
// }


eel.expose(funcUpdateChat);
function funcUpdateChat(data) {
  // console.log(data);
  var d = new Date(data["Date"]);
  if (`${d.getMinutes}`.length == 1) { var min = `0${d.getMinutes()}`; } else { var min = d.getMinutes(); }
  if (`${d.getHours()}`.length == 1) { var hr = `0${d.getHours()}`; } else { var hr = d.getHours(); }

  if (data["Role"] == "user") {
    var z = document.createElement('div');
    z.className = 'msg right-msg';
    z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble"> <div class="msg-info"> <div class="msg-info-name"> Arnav Singh </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${data["Data"]} </div> </div>`;
    Chat.appendChild(z);
  }
  else if (data["Role"] == "skeleton4jaris") {
    var z = document.createElement('div');
    z.className = 'msg left-msg';
    z.innerHTML = `<div class="msg-img" style="background-image: url('Assets/Logo.png')"></div> <div class="skeleton-msg-bubble"> <div class="msg-info"> <div class="msg-info-name">JARVIS</div> <div class="msg-info-time">${hr}:${min}</div> </div> <!-- Loading animation block --> <div class="loading-animation-1"></div> <div class="loading-animation-2"></div> <div class="loading-animation-3"></div> <!-- <div class="loading-animation-4"></div> --> </div>`
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

// eel.expose(funcUpdateChat);
// function funcUpdateChat(data) {
//   // console.log(data);
//   var d = new Date(data["Date"]);
//   if (`${d.getMinutes}`.length == 1) { var min = `0${d.getMinutes()}`; } else { var min = d.getMinutes(); }
//   if (`${d.getHours()}`.length == 1) { var hr = `0${d.getHours()}`; } else { var hr = d.getHours(); }

//   if (data["Role"] == "user") {
//     var z = document.createElement('div');
//     z.className = 'msg right-msg';
//     z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble"> <div class="msg-info"> <div class="msg-info-name"> Arnav Singh </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${data["Data"]} </div> </div>`;
//     Chat.appendChild(z);
//   }
//   else {
//     z.className = 'msg left-msg';
//     if (data["Data"] != "skeleton4jaris") {
//       z.innerHTML = `<div class="msg-img"></div> <div class="msg-bubble "> <div class="msg-info"> <div class="msg-info-name"> Jarvis </div> <div class="msg-info-time">${hr}:${min}</div> </div> <div class="msg-text"> ${data["Data"]} </div> </div>`;
//     }
//     if (data["Data"] == "skeleton4jaris") {
//       z.innerHTML = ` <div class="msg-img" style="background-image: url('Assets/Logo.png')"></div> <div class="skeleton-msg-bubble"> <div class="msg-info"> <div class="msg-info-name">JARVIS</div> <div class="msg-info-time">${hr}:${min}</div> </div> <!-- Loading animation block --> <div class="loading-animation-1"></div> <div class="loading-animation-2"></div> <div class="loading-animation-3"></div> <!-- <div class="loading-animation-4"></div> --> </div> `;
//     }
//     Chat.appendChild(z);
//   }
//   Chat.scrollTop = Chat.scrollHeight;
// }

eel.RestoreHistory("1")((data) => {
  for (var i = 0; i < data.length; i++) {
    funcUpdateChat(data[i]);
  }
  Chat.scrollTop = Chat.scrollHeight;
});

function RestoreHistoryUsingJS(data) {
    for (var i = 0; i < data.length; i++) {
      funcUpdateChat(data[i]);
    }
    Chat.scrollTop = Chat.scrollHeight;
  };

// setInterval(() => {
//   fetch("History/history.json")
//     .then(response => response.json())
//     .then(jsonResponse => {
//       // console.log(jsonResponse["1"]["history"])
//       eel.res 
//     });
// }, 500);


let currentHistory = ""; // Holds the latest history data

async function getHistory() {
  try {
    const response = await fetch("History/history.json");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const jsonResponse = await response.json();
    const newHistory = JSON.stringify(jsonResponse["1"]["history"]);
    
    if (currentHistory !== newHistory) {
      RestoreHistoryUsingJS(jsonResponse["1"]["history"]);
      console.log(jsonResponse["1"]["history"]);
      currentHistory = newHistory;
    }
  } catch (error) {
    console.error("Failed to fetch history:", error);
  }
} 

function InfiniteUpdateHistory() {
  setInterval(() => {
    getHistory();
  }, 500); 
}

InfiniteUpdateHistory();
