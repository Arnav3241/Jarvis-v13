function switchToIndex() {
  window.location.href = "index.html";
}

let isPythonLoaded = false; 

async function funcIsPyLoaded() {
  try {
    const response = await fetch("Constants/loaded.json");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const jsonResponse = await response.json();
    console.log(jsonResponse);
    isPyLoaded = jsonResponse["loaded"];
    if (isPyLoaded) {
      switchToIndex();
    }
  } catch (error) {
    console.error("Failed to is py loaded:", error);
  }
} 

function InfiniteCheckIfPythonLoaded() {
  setInterval(() => {
    funcIsPyLoaded();
    console.log("Checking if Python is loaded...");
  }, 500); 
}

InfiniteCheckIfPythonLoaded();