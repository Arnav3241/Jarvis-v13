console.log("🚀🚀🚀 Rclick.js loaded!")

const body = document.querySelector('body'), sidebar = body.querySelector('nav'), toggle = body.querySelector(".toggle");

sidebar.classList.toggle("close");

toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
})


// SRC: https://codepen.io/ntenebruso/pen/QWLzVjY (Custom Scrooll Bar)

// var cursor = document.querySelector('.cursor');
// var cursorinner = document.querySelector('.cursor2');

// document.addEventListener('mousemove', function(e){
//   var x = e.clientX;
//   var y = e.clientY;
//   cursor.style.transform = `translate3d(calc(${e.clientX}px - 50%), calc(${e.clientY}px - 50%), 0)`
// });

// document.addEventListener('mousemove', function(e){
//   var x = e.clientX;
//   var y = e.clientY;
//   cursorinner.style.left = x + 'px';
//   cursorinner.style.top = y + 'px';
// });

// document.addEventListener('mousedown', function(){
//   cursor.classList.add('click');
//   cursorinner.classList.add('cursorinnerhover')
// });

// document.addEventListener('mouseup', function(){
//   cursor.classList.remove('click')
//   cursorinner.classList.remove('cursorinnerhover')
// });
