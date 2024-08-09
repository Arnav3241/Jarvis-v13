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
  
  console.log(input);
  var z = document.createElement('div');
  z.innerHTML = `<div class="msg-img" style="background-image: url('Assets/Avatar.png')"></div>
    <div class="msg-bubble">
      <div class="msg-info">
        <div class="msg-info-name">User</div>
        <div class="msg-info-time">${hr}:${min}</div>
      </div>
      <div class="msg-text">
        ${input}
      </div>
      <div style="position: relative;">
        <div style="position: absolute; width: 30px; height: 30px; border-radius: 50%; background: #1E1F20; top: 18px; right: 28px;"></div>

        <img onclick="eel.SearchGoogleForJS('${input}');"
          src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAcFJREFUSEvV1UuoT1EUBvDfHXiFDExNJEVEDLwiQ24yFMoAI0OUMpABSQqZGl0Tr+7g3iRGSmFgpAghJSZIEQnldZbOrd129v+/u3WLXadTZ317fWt9e+3vDJjgNTDB+f0TBMuxASuxhj9FPcZTXMVoLxV6dTAZJ7C3j4y3sQWvu3AlgoUYbp5FlWcUhRysJZiK+5jfseEJvmMeAhfrInbgZy3BaexLwN9wDGfxtv0+qUl4GNHpVvwodZpLtB43E/AnLMPzSqn+guUEF7A9Qe3G0HiTx76c4C5WtAk/YlaWfFozrtf7EB7FjTFMTvAOs9tgjN+6LNkMhGy91gGcLBG8wpw2eAdrx0EQA3KmRHAFm9vgF0zHr4SkS6LoeHGC2dZM1+USQeh3KAHvwrk+kpzC/gQzFy9KBBF8lFyiD1iKlwWSJYizmtnGH2bddLppXPnjScL3TUU7EfKNrfCpPTiSTVqM+KW0mC4vilt6r8OHguhZMyExSWEVU7KurmFT3mnJ7BY00ow01cS7Zt3CID7XEgQuZAip0gPM939FeFf4Uqcf1fzRwos2YjVWtbf/QfuzOY83vVqsIaiRqIj5/wl+A2MwRxkhHnjuAAAAAElFTkSuQmCC"
          style="filter: invert(95%) sepia(4%) saturate(112%) hue-rotate(88deg) brightness(83%) contrast(93%); position: absolute; top: 26px; right: 35px; cursor: pointer; width: 15px; height: 15px;" />

        <div style="position: absolute; width: 30px; height: 30px; border-radius: 50%; background: #1E1F20; top: 18px; right: -8px;"></div>

        <img onclick="eel.CopyToClipboardForJS('${input}');"')"
          src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAALVJREFUSEvtlUEKgzAURJ+ncCEUigu9jZdx0xu0F+pBuulOFFx4C0uglSiJTGLdxW3m/xcyw5hx8pedvB8F0AB3oBYv8wZa4Gn0CmACcnH5T9YBpQqYv1PKZYx0pVeGEmCx71BarBB4PRiBIjYtCuCQmQngssb3pF6TYz1wwXvguq2KfwFewM1VdrGA3bqxDxPAWQL2Ew3AJbAqlrT45myAKbsHUImQVVoUgLg3TKb80cI2btQfFJQ0GYp/KrgAAAAASUVORK5CYII="
          style="filter: invert(95%) sepia(4%) saturate(112%) hue-rotate(88deg) brightness(83%) contrast(93%); position: absolute; top: 25px; right: 0px; cursor: pointer; width: 15px; height: 15px;" />
      </div>
    </div>`;
  
  Chat.appendChild(z);
  // eel.AddToUserHistory(input, d, "1");
  Chat.scrollTop = Chat.scrollHeight;

  eel.eelExecuteQuery(input);
});

ChatHistory = []

eel.expose(funcUpdateChat);
function funcUpdateChat(data) {
  // console.log(data);
  var d = new Date(data["Date"]);
  if (`${d.getMinutes}`.length == 1) { var min = `0${d.getMinutes()}`; } else { var min = d.getMinutes(); }
  if (`${d.getHours()}`.length == 1) { var hr = `0${d.getHours()}`; } else { var hr = d.getHours(); }

  if (data["Role"] == "user") {
    var z = document.createElement('div');
    z.className = 'msg right-msg';
    z.innerHTML = `<div class="msg-img" style="background-image: url('Assets/Avatar.png')"></div>
          <div class="msg-bubble">
            <div class="msg-info">
              <div class="msg-info-name">User</div>
              <div class="msg-info-time">${hr}:${min}</div>
            </div>
            <div class="msg-text">
              ${data["Data"]}
            </div>
            <div style="position: relative;">
              <div style="position: absolute; width: 30px; height: 30px; border-radius: 50%; background: #1E1F20; top: 18px; right: 28px;"></div>

              <img onclick="eel.SearchGoogleForJS('${data["Data"]}');"
                src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAcFJREFUSEvV1UuoT1EUBvDfHXiFDExNJEVEDLwiQ24yFMoAI0OUMpABSQqZGl0Tr+7g3iRGSmFgpAghJSZIEQnldZbOrd129v+/u3WLXadTZ317fWt9e+3vDJjgNTDB+f0TBMuxASuxhj9FPcZTXMVoLxV6dTAZJ7C3j4y3sQWvu3AlgoUYbp5FlWcUhRysJZiK+5jfseEJvmMeAhfrInbgZy3BaexLwN9wDGfxtv0+qUl4GNHpVvwodZpLtB43E/AnLMPzSqn+guUEF7A9Qe3G0HiTx76c4C5WtAk/YlaWfFozrtf7EB7FjTFMTvAOs9tgjN+6LNkMhGy91gGcLBG8wpw2eAdrx0EQA3KmRHAFm9vgF0zHr4SkS6LoeHGC2dZM1+USQeh3KAHvwrk+kpzC/gQzFy9KBBF8lFyiD1iKlwWSJYizmtnGH2bddLppXPnjScL3TUU7EfKNrfCpPTiSTVqM+KW0mC4vilt6r8OHguhZMyExSWEVU7KurmFT3mnJ7BY00ow01cS7Zt3CID7XEgQuZAip0gPM939FeFf4Uqcf1fzRwos2YjVWtbf/QfuzOY83vVqsIaiRqIj5/wl+A2MwRxkhHnjuAAAAAElFTkSuQmCC"
                style="filter: invert(95%) sepia(4%) saturate(112%) hue-rotate(88deg) brightness(83%) contrast(93%); position: absolute; top: 26px; right: 35px; cursor: pointer; width: 15px; height: 15px;" />

              <div style="position: absolute; width: 30px; height: 30px; border-radius: 50%; background: #1E1F20; top: 18px; right: -8px;"></div>

              <img onclick="eel.CopyToClipboardForJS('${data["Data"]}');"')"
                src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAALVJREFUSEvtlUEKgzAURJ+ncCEUigu9jZdx0xu0F+pBuulOFFx4C0uglSiJTGLdxW3m/xcyw5hx8pedvB8F0AB3oBYv8wZa4Gn0CmACcnH5T9YBpQqYv1PKZYx0pVeGEmCx71BarBB4PRiBIjYtCuCQmQngssb3pF6TYz1wwXvguq2KfwFewM1VdrGA3bqxDxPAWQL2Ew3AJbAqlrT45myAKbsHUImQVVoUgLg3TKb80cI2btQfFJQ0GYp/KrgAAAAASUVORK5CYII="
                style="filter: invert(95%) sepia(4%) saturate(112%) hue-rotate(88deg) brightness(83%) contrast(93%); position: absolute; top: 25px; right: 0px; cursor: pointer; width: 15px; height: 15px;" />
            </div>
          </div>`;
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
    z.innerHTML = `<div class="msg-img" style="background-image: url('Assets/Logo.png')"></div>
      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">JARVIS</div>
          <div class="msg-info-time">${hr}:${min}</div>
        </div>
        <div class="msg-text">
          ${data["Data"]}
        </div>
        <div style="position: relative;"
              onclick="eel.CopyToClipboardForJS('${data["Data"]}');">
              <div style="position: absolute; width: 30px; height: 30px; border-radius: 50%; background: #1E1F20; transform: translate(-7px, 17px);"></div>
              <img
                src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAALVJREFUSEvtlUEKgzAURJ+ncCEUigu9jZdx0xu0F+pBuulOFFx4C0uglSiJTGLdxW3m/xcyw5hx8pedvB8F0AB3oBYv8wZa4Gn0CmACcnH5T9YBpQqYv1PKZYx0pVeGEmCx71BarBB4PRiBIjYtCuCQmQngssb3pF6TYz1wwXvguq2KfwFewM1VdrGA3bqxDxPAWQL2Ew3AJbAqlrT45myAKbsHUImQVVoUgLg3TKb80cI2btQfFJQ0GYp/KrgAAAAASUVORK5CYII="
                style="filter: invert(95%) sepia(4%) saturate(112%) hue-rotate(88deg) brightness(83%) contrast(93%); position: absolute; transform: translate(0px, 25px); cursor: pointer; width: 15px; height: 15px;"
                id="yoyohanisingh" />
            </div>
      </div>`;
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

// eel.RestoreHistory("1")((data) => {
//   for (var i = 0; i < data.length; i++) {
//     funcUpdateChat(data[i]);
//   }
//   Chat.scrollTop = Chat.scrollHeight;
// });

function RestoreHistoryUsingJS(data) {
  Chat.innerHTML = "";
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
      console.log("New history found");
      RestoreHistoryUsingJS(jsonResponse["1"]["history"]);
      console.log(jsonResponse["1"]["history"]);
      currentHistory = newHistory;
      console.log(currentHistory);
    }
  } catch (error) {
    console.error("Failed to fetch history:", error);
  }
}

function InfiniteUpdateHistory() {
  setInterval(() => {
    getHistory();
  }, 100);
}

InfiniteUpdateHistory();
