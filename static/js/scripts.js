document.addEventListener("DOMContentLoaded", () => {
    actualizarContadorCarrito();

    const pageCatalog = document.getElementById("pageCatalog");
    const pageCart = document.getElementById("pageCart");
    const pageAccount = document.getElementById("pageAccount");
    const pageAdmin = document.getElementById("pageAdmin");

    // --- INICIALIZACIÓN POR PÁGINA ---
    if (pageCatalog) initCatalogPage();
    if (pageCart) initCartPage();
    if (pageAccount) initAccountPage();
    if (pageAdmin) initAdminPage();
});

// --- CARRITO ---
async function actualizarContadorCarrito() {
    try {
        const res = await fetch("/carrito-gestion");
        const data = await res.json();
        const badge = document.getElementById("cartCount");
        if (badge) badge.textContent = data.cantidad || 0;
    } catch (e) { console.error("Error contador:", e); }
}

async function añadirAlCarrito(id) {
    try {
        const res = await fetch("/carrito-gestion", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id })
        });
        
        if (res.ok) {
            await actualizarContadorCarrito();
            // El toast vuelve a funcionar al llamar a la función definida al final[cite: 27]
            mostrarToast("¡Libro añadido al carrito!", "success");
        } else {
            mostrarToast("No se pudo añadir el libro", "error");
        }
    } catch (e) { 
        console.error("Error al añadir:", e);
        mostrarToast("Error de conexión con el servidor", "error");
    }
}

// --- CATÁLOGO, FILTROS Y BÚSQUEDA ---
async function initCatalogPage() {
    // Inicializar los listeners de los filtros[cite: 27]
    setupFilters();
    // Carga inicial de datos
    await cargarCatalogoFiltrado();
}

function setupFilters() {
    const qInput = document.getElementById("q");
    const categorySelect = document.getElementById("category");
    const sortSelect = document.getElementById("sort");
    const btnClear = document.getElementById("btnClear");

    if (!qInput || !categorySelect || !sortSelect) return;

    // Búsqueda con debounce para no saturar el servidor
    let timeout = null;
    qInput.addEventListener("input", () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => cargarCatalogoFiltrado(), 300);
    });

    categorySelect.addEventListener("change", cargarCatalogoFiltrado);
    sortSelect.addEventListener("change", cargarCatalogoFiltrado);

    if (btnClear) {
        btnClear.addEventListener("click", () => {
            qInput.value = "";
            categorySelect.value = "";
            sortSelect.value = "";
            cargarCatalogoFiltrado();
        });
    }
}

async function cargarCatalogoFiltrado() {
    const q = document.getElementById("q")?.value || "";
    const category = document.getElementById("category")?.value || "";
    const sort = document.getElementById("sort")?.value || "";

    const params = new URLSearchParams({ q, category, sort });

    try {
        const res = await fetch(`/libros-data?${params.toString()}`);
        const libros = await res.json();
        renderizarLibros(libros);
    } catch (e) {
        console.error("Error al filtrar:", e);
    }
}

function renderizarLibros(libros) {
    const catalogo = document.getElementById("catalogo");
    const template = document.getElementById("cardTemplate");
    if (!catalogo || !template) return;

    catalogo.innerHTML = "";
    libros.forEach(libro => {
        const clone = template.content.cloneNode(true);
        clone.querySelector("[data-title]").textContent = libro.titulo;
        clone.querySelector("[data-author]").textContent = libro.autor;
        clone.querySelector("[data-category]").textContent = libro.categoria;
        clone.querySelector("[data-price]").textContent = `${parseFloat(libro.precio).toFixed(2)} €`;
        
        // Gestión de imagen: Si falla la ruta de la DB, carga placeholder[cite: 27]
        const img = clone.querySelector("[data-img]");
        img.src = libro.imagen_url || '/static/uploads/default_book.png';
        img.onerror = () => { img.src = "https://via.placeholder.com/150?text=Sin+Portada"; };

        const btn = clone.querySelector("button");
        btn.onclick = () => añadirAlCarrito(libro.id);

        catalogo.appendChild(clone);
    });
}

// --- VISTA DEL CARRITO ---
async function initCartPage() {
    try {
        const res = await fetch("/carrito-gestion");
        const data = await res.json();
        const lista = document.getElementById("cartList");
        const totalElt = document.getElementById("cartTotal");
        if (!lista) return;

        if (!data.items || data.items.length === 0) {
            lista.innerHTML = `<div class="empty">Tu carrito está vacío. <a href="/" class="link">Volver al catálogo</a></div>`;
        } else {
            lista.innerHTML = "";
            data.items.forEach(item => {
                const itemDiv = document.createElement("div");
                itemDiv.className = "cart-item";
                itemDiv.innerHTML = `
                    <img src="${item.imagen_url}" alt="${item.titulo}" onerror="this.src='https://via.placeholder.com/150'">
                    <div class="info-container">
                        <p class="title">${item.titulo}</p>
                        <p class="price-unit">${parseFloat(item.precio).toFixed(2)} € / ud.</p>
                    </div>
                    <div class="qty-controls">
                        <button onclick="cambiarCantidad(${item.id}, -1)">-</button>
                        <span class="qty-val">${item.cantidad}</span>
                        <button onclick="cambiarCantidad(${item.id}, 1)">+</button>
                    </div>
                    <div class="subtotal-val">
                        ${(item.precio * item.cantidad).toFixed(2)} €
                    </div>
                `;
                lista.appendChild(itemDiv);
            });
        }
        if (totalElt) totalElt.textContent = `${data.total.toFixed(2)} €`;
    } catch (e) { console.error("Error al cargar carrito:", e); }
}

async function cambiarCantidad(id, cambio) {
    try {
        const resPre = await fetch("/carrito-gestion");
        const dataPre = await resPre.json();
        const itemAntes = dataPre.items.find(item => String(item.id) === String(id));

        const res = await fetch("/carrito/actualizar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id, cambio })
        });

        if (res.ok) {
            await actualizarContadorCarrito();
            initCartPage();

            if (itemAntes && itemAntes.cantidad === 1 && cambio === -1) {
                mostrarToast("Libro eliminado del carrito", "error");
            } 
        }
    } catch (e) {
        mostrarToast("No se pudo actualizar el carrito", "error");
    }
}

// --- NOTIFICACIONES (TOAST) ---
function mostrarToast(mensaje, tipo = 'success') {
    let container = document.getElementById("toastContainer");
    
    // Si el contenedor no existe por algún motivo, lo creamos dinámicamente
    if (!container) {
        container = document.createElement("div");
        container.id = "toastContainer";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast ${tipo}`;
    toast.textContent = mensaje;

    // Estilos de borde dinámicos[cite: 27]
    if (tipo === 'error') toast.style.borderLeft = "5px solid #e74c3c";
    else toast.style.borderLeft = "5px solid #2ecc71";

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// --- PAGO Y SESIÓN ---
async function iniciarPago() {
    const btn = document.getElementById("btnPagar");
    if (!btn) return;
    
    btn.disabled = true;
    btn.textContent = "Procesando...";

    try {
        const res = await fetch("/crear-checkout", { method: "POST" });
        if (res.redirected) {
            window.location.href = res.url;
            return;
        }

        const data = await res.json();
        if (data.url) {
            window.location.href = data.url;
        } else {
            mostrarToast(data.error || "Error al iniciar el pago", "error");
            btn.disabled = false;
            btn.textContent = "Pagar ahora";
        }
    } catch (e) {
        mostrarToast("Error de conexión", "error");
        btn.disabled = false;
    }
}

// Exponer funciones globales necesarias para onclick en el HTML[cite: 27]
window.cambiarCantidad = cambiarCantidad;
window.iniciarPago = iniciarPago;
window.añadirAlCarrito = añadirAlCarrito;