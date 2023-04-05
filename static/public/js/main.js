// FORM'S JS
function adjustNavClass() {
    var nav = document.getElementById("nav");
    if (window.innerWidth < 900) {
      nav.classList.remove("justify-content-end");
      nav.classList.add("justify-content-center");
    } else {
      nav.classList.remove("justify-content-center");
      nav.classList.add("justify-content-end");
    }
  }

  function activateNavLink() {
    let title = document.getElementById("title");
    console.log(title.value);
    var active;
    
    if (title.value == "index") {

    } else if (title.value == 'Iniciar sesión') {
      active = document.getElementById('login');
      active.classList.add('active','bg-primary','bg-gradient','border-0','rounded-pill');
    } else if (title.value == 'Registrarse') {
      active = document.getElementById('signup');
      active.classList.add('active','bg-primary','bg-gradient','border-0','rounded-pill');
    }
  }

// Call the function once on page load
adjustNavClass();
activateNavLink();

// Call the function every time the window size changes
window.addEventListener("resize", adjustNavClass);
// ------------------------------------------------------------------------------------------