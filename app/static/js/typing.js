const roles = ["Benno👋", "Softwareentwickler", "Data Scientist"];

let count = 0;
let index = 0;
let isDeleting = false;

function typeRole() {
  const nameEl = document.getElementById("typed-name");

  // Falls Element nicht existiert → Script stoppt (wichtig für andere Pages!)
  if (!nameEl) return;

  const currentText = roles[count];

  if (!isDeleting) {
    nameEl.textContent = currentText.slice(0, index + 1);
    index++;

    if (index === currentText.length) {
      isDeleting = true;
      setTimeout(typeRole, 1500);
      return;
    }
    setTimeout(typeRole, 75);
  } else {
    nameEl.textContent = currentText.slice(0, index - 1);
    index--;

    if (index === 0) {
      isDeleting = false;
      count = (count + 1) % roles.length;
      setTimeout(typeRole, 300);
      return;
    }
    setTimeout(typeRole, 50);
  }
}

// Start erst wenn DOM geladen ist
document.addEventListener("DOMContentLoaded", typeRole);