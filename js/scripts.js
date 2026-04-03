document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  actualizarContadorCarrito(); // Se ejecuta en todas las páginas

  // Detectar en qué página estamos para ejecutar su lógica específica
  if (document.getElementById("pageCatalog")) {
    initCatalogPage();
  } else if (document.getElementById("pageCart")) {
    initCartPage();
  }
});

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

    clone.querySelector("[data-title]").textContent = book.titulo;
    clone.querySelector("[data-author]").textContent = book.autor;
    clone.querySelector("[data-category]").textContent = book.categoria;
    clone.querySelector("[data-price]").textContent = `${parseFloat(book.precio).toFixed(2)} €`;

    const img = clone.querySelector("[data-img]");
    if (img && book.imagen_url && book.imagen_url !== "#") {
      img.src = book.imagen_url;
      img.alt = book.titulo;
      img.style.display = "block";
    } else if (img) {
      img.style.display = "none";
    }

    // EVENTO PARA AÑADIR AL CARRITO (Conecta con Python)
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
    const response = await fetch('http://127.0.0.1:5000/api/carrito');
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

    // Rellenar visualmente el carrito usando lo que ya teníais en el CSS
    data.items.forEach(item => {
      cartList.innerHTML += `
                <div class="cart-item">
                    <img src="${item.imagen_url !== '#' ? item.imagen_url : ''}" alt="${item.titulo}" onerror="this.style.display='none'">
                    <div>
                        <div class="title">${item.titulo}</div>
                        <div class="price">${parseFloat(item.precio).toFixed(2)} €</div>
                    </div>
                </div>
            `;
    });

    // Botón de vaciar carrito
    const btnClearCart = document.getElementById("btnClearCart");
    if (btnClearCart) {
      btnClearCart.addEventListener("click", async () => {
        await fetch('http://127.0.0.1:5000/api/carrito/clear', { method: 'POST' });
        initCartPage(); // Recargar la página del carrito
        actualizarContadorCarrito(); // Poner el globito a 0
      });
    }

  } catch (error) {
    console.error("Error cargando la vista del carrito:", error);
  }
}

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