// function showLogin() {
//   document.getElementById("loginModal").style.display = "flex";
// }

// function hideLogin() {
//   document.getElementById("loginModal").style.display = "none";
// }

// function showSignup() {
//   document.getElementById("signupModal").style.display = "flex";
// }

// function hideSignup() {
//   document.getElementById("signupModal").style.display = "none";
// }
function OpenPopup() {
  let popup = document.getElementById("PopupOverlay");
  popup.classList.remove("opacity-0", "invisible");
  popup.classList.add("opacity-100", "visible");

  let popupBox = popup.querySelector("div");
  popupBox.classList.replace("scale-95", "scale-100");
}


function ClosePopup() {
  let popup = document.getElementById("PopupOverlay");
  popup.classList.replace("opacity-100", "opacity-0");

  let popupBox = popup.querySelector("div");
  popupBox.classList.replace("scale-100", "scale-95");

  setTimeout(() => {
      popup.classList.replace("visible", "invisible");
  }, 300);
}


function openPopup() {
      document.getElementById("popupOverlay").classList.remove("opacity-0", "invisible");
      document.querySelector(".scale-95").classList.replace("scale-95", "scale-100");
}

function closePopup() {
      document.getElementById("popupOverlay").classList.add("opacity-0", "invisible");
      document.querySelector(".scale-100").classList.replace("scale-100", "scale-95");
}