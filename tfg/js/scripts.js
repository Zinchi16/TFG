// ==========================================
// ARRANQUE PRINCIPAL DE LA WEB
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  actualizarContadorCarrito();
  gestionarEstadoSesion(); // Comprueba si hay alguien logueado

  // Detectar en qué página estamos para arrancar su "motor" específico
  if (document.getElementById("pageCatalog")) {
    initCatalogPage(); // Esto es lo que pinta los libros
  } else if (document.getElementById("pageCart")) {
    initCartPage(); // Esto pinta el carrito
  } else if (document.getElementById("pageAccount")) {
    initAccountPage(); // Esto arranca el login/registro
  }
});

function gestionarEstadoSesion() {
  // 1. Intentamos buscar por ID (linkCuenta)
  let linkCuenta = document.getElementById("linkCuenta");

  // 2. PLAN B: Si no lo encuentra, busca cualquier enlace que contenga "cuenta.html"
  if (!linkCuenta) {
    linkCuenta = document.querySelector('a[href*="cuenta.html"]');
  }

  const usuario = JSON.parse(localStorage.getItem("usuario"));

  if (usuario && linkCuenta) {
    // Si el usuario existe, transformamos el botón
    linkCuenta.textContent = "Cerrar sesión";
    linkCuenta.href = "#"; // Rompemos el enlace normal
    linkCuenta.onclick = cerrarSesion; // Le damos el poder de borrar todo
  }
}
// ==========================================
// 1. LÓGICA DEL CATÁLOGO Y FILTROS
// ==========================================
async function initCatalogPage() {
  // Primera carga sin filtros
  await fetchLibrosDesdePython();
  setupFilters();
}

// Nueva función que envía los filtros al Backend
async function fetchLibrosDesdePython() {
  const q = document.getElementById("q")?.value || "";
  const category = document.getElementById("category")?.value || "";
  const sort = document.getElementById("sort")?.value || "";

  // Construimos la URL con los parámetros para Python
  const url = new URL('http://127.0.0.1:5000/api/libros');
  if (q) url.searchParams.append('q', q);
  if (category) url.searchParams.append('category', category);
  if (sort) url.searchParams.append('sort', sort);

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error("Error en el servidor");
    const books = await response.json();
    renderCatalog(books);
  } catch (error) {
    console.error(error);
    document.getElementById("emptyState").hidden = false;
  }
}

function renderCatalog(books) {
  const catalog = document.getElementById("catalogo");
  const template = document.getElementById("cardTemplate");
  const emptyState = document.getElementById("emptyState");

  if (!catalog || !template) return;

  catalog.innerHTML = "";

  if (books.length === 0) {
    emptyState.hidden = false;
    return;
  } else {
    emptyState.hidden = true;
  }

  books.forEach(book => {
    const clone = template.content.cloneNode(true);

    // Mapeo de datos
    clone.querySelector("[data-title]").textContent = book.titulo;
    clone.querySelector("[data-author]").textContent = book.autor;
    clone.querySelector("[data-category]").textContent = book.categoria;
    clone.querySelector("[data-price]").textContent = `${parseFloat(book.precio).toFixed(2)} €`;

    // CONTROL DE LA IMAGEN (Aquí está la magia de la ruta)
    const img = clone.querySelector("[data-img]");
    if (img && book.imagen_url && book.imagen_url !== "#") {
      img.src = 'http://127.0.0.1:5000' + book.imagen_url;
      img.alt = book.titulo;
      img.style.display = "block";
    } else if (img) {
      img.style.display = "none";
    }

    // EVENTO PARA AÑADIR AL CARRITO
    const btnAdd = clone.querySelector("[data-add]");
    if (btnAdd) {
      btnAdd.addEventListener("click", () => añadirAlCarrito(book.id));
    }

    catalog.appendChild(clone);
  });
}

function setupFilters() {
  const elementos = ["q", "category", "sort"];

  // Cada vez que se toca un filtro, JS le pide a Python que vuelva a buscar
  elementos.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener(id === "q" ? "input" : "change", fetchLibrosDesdePython);
    }
  });

  const btnClear = document.getElementById("btnClear");
  if (btnClear) {
    btnClear.addEventListener("click", () => {
      elementos.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
      });
      fetchLibrosDesdePython();
    });
  }
}


// ==========================================
// 2. LÓGICA DEL CARRITO (Conecta con Python)
// ==========================================
async function añadirAlCarrito(libro_id) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/carrito/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: libro_id })
    });
    const data = await response.json();

    // Actualizamos el globito del header
    if (data.cantidad !== undefined) {
      document.getElementById("cartCount").textContent = data.cantidad;
    }
  } catch (error) {
    console.error("Error al añadir al carrito:", error);
  }
}

async function actualizarContadorCarrito() {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/carrito');
    const data = await response.json();
    const cartCount = document.getElementById("cartCount");
    if (cartCount) cartCount.textContent = data.cantidad || 0;
  } catch (error) {
    console.error("No se pudo cargar el carrito:", error);
  }
}

// Lógica para la página carrito.html
async function initCartPage() {
  try {
    const cacheBuster = new Date().getTime();
    const response = await fetch(`http://127.0.0.1:5000/api/carrito?t=${cacheBuster}`);
    const data = await response.json();

    const cartList = document.getElementById("cartList");
    const cartEmpty = document.getElementById("cartEmpty");
    const cartSummary = document.getElementById("cartSummary");
    const cartTotal = document.getElementById("cartTotal");

    if (!cartList) return;

    cartList.innerHTML = "";

    if (data.items.length === 0) {
      cartEmpty.hidden = false;
      cartSummary.hidden = true;
      return;
    }

    cartEmpty.hidden = true;
    cartSummary.hidden = false;
    cartTotal.textContent = `${parseFloat(data.total).toFixed(2)} €`;

    // Dibujamos cada libro del carrito
    data.items.forEach(item => {
      cartList.innerHTML += `
                <div class="cart-item">
                    <img src="${item.imagen_url !== '#' ? 'http://127.0.0.1:5000' + item.imagen_url : ''}" alt="${item.titulo}" onerror="this.style.display='none'">
                    <div style="flex-grow: 1;">
                        <div class="title">${item.titulo}</div>
                        <div class="price">${parseFloat(item.precio).toFixed(2)} €</div>
                    </div>
                    <button class="btn btn-danger" onclick="quitarLibroIndividual('${item.id}')" style="padding: 6px 12px; font-size: 0.9rem;">Eliminar</button>
                </div>
            `;
    });

    // Botón de vaciar carrito completo
    const btnClearCart = document.getElementById("btnClearCart");
    if (btnClearCart) {
      btnClearCart.onclick = async () => {
        if (confirm("¿Seguro que quieres vaciar todo el carrito?")) {
          await fetch('http://127.0.0.1:5000/api/carrito/clear', { method: 'POST' });
          initCartPage();
          actualizarContadorCarrito();
        }
      };
    }

    // --- EL PORTERO: Lógica del botón Finalizar Compra ---
    const btnFinalizarCompra = document.getElementById("btnFinalizarCompra");
    if (btnFinalizarCompra) {
      btnFinalizarCompra.onclick = (e) => {
        const usuario = JSON.parse(localStorage.getItem("usuario"));

        if (!usuario) {
          // No hay sesión: bloqueamos el botón y mandamos al login
          e.preventDefault();
          alert("¡Alto ahí! Para poder finalizar tu compra, primero debes iniciar sesión.");
          window.location.href = "cuenta.html";
        } else {
          // Sí hay sesión: dejamos pasar
          alert(`¡Gracias por tu pedido, ${usuario.nombre}! Procesando compra...`);
        }
      };
    }

  } catch (error) {
    console.error("Error cargando la vista del carrito:", error);
  }
}

// Conecta el botón de Eliminar con Python
window.quitarLibroIndividual = async function (id) {
  try {
    await fetch(`http://127.0.0.1:5000/api/carrito/remove/${id}`, { method: 'DELETE' });
    // Volvemos a pintar el carrito inmediatamente después de borrar
    initCartPage();
    actualizarContadorCarrito();
  } catch (error) {
    console.error("Error al quitar libro:", error);
  }
};

// ==========================================
// 3. UTILIDADES GENERALES
// ==========================================
function initTheme() {
  const btn = document.getElementById("toggleTheme");
  const html = document.documentElement;
  const savedTheme = localStorage.getItem("theme") || "light";
  html.className = savedTheme;

  if (btn) {
    btn.addEventListener("click", () => {
      const isDark = html.classList.toggle("dark");
      localStorage.setItem("theme", isDark ? "dark" : "light");
      btn.querySelector("span").textContent = isDark ? "Modo claro" : "Modo oscuro";
    });
  }
}
// ==========================================
// 4. LÓGICA DE USUARIOS (LOGIN/REGISTRO)
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
  // Detectar si estamos en la página de cuenta para ejecutar la lógica
  if (document.getElementById("pageAccount")) {
    initAccountPage();
  }
});

function initAccountPage() {
  const loginSection = document.getElementById("loginSection");
  const registerSection = document.getElementById("registerSection");

  // Cambiar entre pantalla de login y registro
  document.getElementById("linkToRegister").addEventListener("click", (e) => {
    e.preventDefault();
    loginSection.hidden = true;
    registerSection.hidden = false;
  });

  document.getElementById("linkToLogin").addEventListener("click", (e) => {
    e.preventDefault();
    registerSection.hidden = true;
    loginSection.hidden = false;
  });

  // Función de Login
  const btnLogin = document.getElementById("btnLogin");
  if (btnLogin) {
    btnLogin.addEventListener("click", async () => {
      const email = document.getElementById("loginEmail").value;
      const password = document.getElementById("loginPassword").value;
      const errorBox = document.getElementById("loginError");

      try {
        const response = await fetch('http://127.0.0.1:5000/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await response.json();

        if (response.ok) {
          // GUARDAMOS AL USUARIO EN EL NAVEGADOR
          // Dentro de la función de login, cuando la respuesta es OK:
          localStorage.setItem("usuario", JSON.stringify({ nombre: data.nombre }));
          alert("¡Bienvenido " + data.email + "!");
          window.location.href = "index.html"; // Redirige al catálogo
        } else {
          errorBox.textContent = data.error;
          errorBox.hidden = false;
        }
      } catch (err) {
        errorBox.textContent = "Error de conexión con el servidor";
        errorBox.hidden = false;
      }
    });
  }

  // Función de Registro
  const btnRegister = document.getElementById("btnRegister");
  if (btnRegister) {
    btnRegister.addEventListener("click", async () => {
      const email = document.getElementById("regEmail").value;
      const password = document.getElementById("regPassword").value;
      const msgBox = document.getElementById("registerMsg");

      try {
        const response = await fetch('http://127.0.0.1:5000/api/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await response.json();

        if (response.ok) {
          msgBox.style.color = "var(--success)";
          msgBox.textContent = "¡Cuenta creada! Ya puedes iniciar sesión.";
          msgBox.hidden = false;
        } else {
          msgBox.style.color = "var(--danger)";
          msgBox.textContent = data.error;
          msgBox.hidden = false;
        }
      } catch (err) {
        msgBox.style.color = "var(--danger)";
        msgBox.textContent = "Error de conexión con el servidor";
        msgBox.hidden = false;
      }
    });
  }
}
async function cerrarSesion(e) {
  if (e) e.preventDefault();

  if (confirm("¿Quieres cerrar tu sesión? Se vaciará tu carrito.")) {
    try {
      // 1. Vaciamos el carrito en el servidor Python
      await fetch('http://127.0.0.1:5000/api/carrito/clear', { method: 'POST' });

      // 2. Borramos los datos del usuario en el navegador
      localStorage.removeItem("usuario");

      // 3. Limpiar datos locales del carrito si tuvieras
      alert("Sesión cerrada y carrito vaciado.");

      // 4. Redirigimos al catálogo para refrescar la interfaz
      window.location.href = "index.html";
    } catch (error) {
      console.error("Error al cerrar sesión:", error);
    }
  }
}