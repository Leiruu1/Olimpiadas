var supabaseUrl = 'https://ypcmagomeuglwqsdvbfo.supabase.co';
var supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlwY21hZ29tZXVnbHdxc2R2YmZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExNDQyMjAsImV4cCI6MjA2NjcyMDIyMH0.kyHAHetXieBxtY9sSgAEqqJ0G9t-iOwiS6fJMDb-Df4';
var supabase = supabase.createClient(supabaseUrl, supabaseKey);

let carrito = [];

function addToCart(nombre, precio) {
  const index = carrito.findIndex(item => item.nombre === nombre);
  if (index !== -1) {
    carrito[index].cantidad++;
  } else {
    carrito.push({ nombre, precio, cantidad: 1 });
  }
  actualizarCartModal();
  alert(`${nombre} agregado al carrito`);
}

function mostrarFormularioAgregar() {
  document.getElementById("formularioAgregar").style.display = "block";
}

function actualizarCartModal() {
  const lista = document.getElementById('cartItems');
  const total = document.getElementById('cartTotal');
  lista.innerHTML = '';

  if (carrito.length === 0) {
    lista.innerHTML = '<li class="list-group-item text-center text-muted">Tu carrito está vacío.</li>';
    total.textContent = `$0`;
    return;
  }

  let suma = 0;

  carrito.forEach((item, index) => {
    const subtotal = item.precio * item.cantidad;
    suma += subtotal;

    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between align-items-center';

    li.innerHTML = `
      <div>
        ${item.nombre}
      </div>
      <div>
        <input type="number" min="1" value="${item.cantidad}" data-index="${index}" class="cantidad-input" style="width: 60px; margin-right: 10px;">
        <span class="fw-bold text-warning me-3">$${subtotal.toFixed(2)}</span>
        <button class="btn btn-sm btn-outline-danger" onclick="eliminarItem(${index})">✖</button>
      </div>
    `;

    lista.appendChild(li);
  });

  total.textContent = `$${suma.toFixed(2)}`;

  document.querySelectorAll('.cantidad-input').forEach(input => {
    input.addEventListener('change', e => {
      const idx = e.target.getAttribute('data-index');
      let val = parseInt(e.target.value);
      if (isNaN(val) || val < 1) val = 1;
      carrito[idx].cantidad = val;
      actualizarCartModal();
    });
  });
}

function eliminarItem(index) {
  carrito.splice(index, 1);
  actualizarCartModal();
}

function finalizarReserva() {
  const user = localStorage.getItem("loggedInUser");
  if (!user) {
    alert('Debés iniciar sesión para finalizar la reserva.');
    window.location.href = 'inicio.html';
    return;
  }

  if (carrito.length === 0) {
    alert('Tu carrito está vacío.');
    return;
  }

  const mensaje = carrito.map(i => `• ${i.nombre} (x${i.cantidad}) - $${(i.precio * i.cantidad).toFixed(2)}`).join('\n');
  const total = carrito.reduce((suma, item) => suma + item.precio * item.cantidad, 0);

  localStorage.setItem('carrito', JSON.stringify(carrito));
  localStorage.setItem('mensaje', mensaje);
  localStorage.setItem('total', total);

  alert('Reserva finalizada. Gracias por tu compra!');

  setTimeout(() => {
    window.location.href = 'confirmation.html';
  }, 100);
}

function addToCartFromDOM(button) {
  const tarjeta = button.closest('.tarjeta');
  const nombre = tarjeta.dataset.nombre;
  const precio = parseFloat(tarjeta.dataset.precio);
  addToCart(nombre, precio);
}

async function validarSesion() {
  const { data: { session } } = await supabase.auth.getSession();

  const loginBtn = document.getElementById('loginButton');
  if (!loginBtn) return;

  if (session) {
    const user = session.user;
    loginBtn.textContent = 'Cerrar sesión';
    loginBtn.className = 'btn btn-danger';
    loginBtn.onclick = async () => {
      await supabase.auth.signOut();
      window.location.reload();
    };
    localStorage.setItem('loggedInUser', JSON.stringify(user));
  } else {
    loginBtn.textContent = 'Iniciar sesión';
    loginBtn.className = 'btn btn-primary';
    loginBtn.onclick = () => {
      window.location.href = 'inicio.html';
    };
    localStorage.removeItem('loggedInUser');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  validarSesion();

  // Listener para botón finalizar compra
  const btnFinalizar = document.getElementById('finalizarCompraBtn');
  if (btnFinalizar) {
    btnFinalizar.addEventListener('click', finalizarReserva);
  }
});

function eliminarProducto(botonEliminar) {
  const tarjeta = botonEliminar.closest('.tarjeta');
  const codigoProducto = tarjeta.getAttribute('data-codigo');
  let productos = JSON.parse(localStorage.getItem('productos')) || [];
  productos = productos.filter(prod => prod.codigo !== codigoProducto);
  localStorage.setItem('productos', JSON.stringify(productos));
  tarjeta.remove();
}

function cargarProductosDesdeStorage() {
  const productos = JSON.parse(localStorage.getItem('productos')) || [];
  const userJSON = localStorage.getItem('loggedInUser');
  let esAdmin = false;
  if (userJSON) {
    const user = JSON.parse(userJSON);
    esAdmin = user.admin || false;
  }
  productos.forEach(producto => mostrarTarjetaProducto(producto, esAdmin));
}

document.getElementById('formAgregar').addEventListener('submit', function(event) {
  event.preventDefault();
  agregarProducto();
});

function agregarProducto() {
  const nombre = document.getElementById('inputNombre').value.trim();
  const categoria = document.getElementById('inputCategoria').value;
  const precio = parseFloat(document.getElementById('inputPrecio').value);
  const codigo = document.getElementById('inputCodigo').value.trim();
  const etiquetas = document.getElementById('inputEtiquetas').value.trim();
  const descripcion = document.getElementById('inputDescripcion').value.trim();

  if (!nombre || !categoria || isNaN(precio) || !codigo || !descripcion) {
    alert('Por favor, completa todos los campos obligatorios.');
    return;
  }

  const producto = { nombre, categoria, precio, codigo, etiquetas, descripcion };

  mostrarTarjetaProducto(producto);

  let productosGuardados = JSON.parse(localStorage.getItem('productos')) || [];
  productosGuardados.push(producto);
  localStorage.setItem('productos', JSON.stringify(productosGuardados));

  document.getElementById('formAgregar').reset();

  alert('Producto agregado con éxito.');
}

window.onload = function () {
  const userJSON = localStorage.getItem('loggedInUser');
  let esAdmin = false;

  if (userJSON) {
    const user = JSON.parse(userJSON);
    esAdmin = user.admin || false;
  }

  const formulario = document.getElementById('formAgregar');
  if (formulario) formulario.style.display = esAdmin ? 'block' : 'none';

  const botonEliminar = document.getElementById('btnEliminar');
  if (botonEliminar) botonEliminar.style.display = esAdmin ? 'inline-block' : 'none';

  let productos = JSON.parse(localStorage.getItem('productos')) || [];
  productos.forEach(producto => mostrarTarjetaProducto(producto, esAdmin));

  const usuario = localStorage.getItem("usuarioLogueado");
  localStorage.setItem("clientePedido", usuario);

  localStorage.setItem("carrito", JSON.stringify(carrito));

  cargarProductosDesdeStorage();
};

function mostrarTarjetaProducto(producto, esAdmin) {
  const tarjeta = document.createElement('div');
  tarjeta.className = 'tarjeta position-relative';

  tarjeta.setAttribute('data-codigo', producto.codigo);
  tarjeta.setAttribute('data-nombre', producto.nombre);
  tarjeta.setAttribute('data-precio', producto.precio);

  let headerColor = '';
  switch (producto.categoria) {
    case 'Hotel':
      headerColor = 'linear-gradient(to right, #00c6ff, #0072ff)';
      break;
    case 'Auto':
      headerColor = 'linear-gradient(to right, #8EC5FC, #E0C3FC)';
      break;
    case 'Paquete':
      headerColor = 'linear-gradient(to right, #f6d365, #fda085)';
      break;
    default:
      headerColor = '#ccc';
  }

  tarjeta.innerHTML = `
    <div class="tarjeta-header" style="background: ${headerColor};">
      <div class="categoria">${producto.categoria}</div>
    </div>
    <div class="p-3">
      <h5>${producto.nombre}</h5>
      <p>${producto.descripcion}</p>
      <div class="etiquetas mb-2">
        ${producto.etiquetas.split(' ').map(et => `<span class="${et}">${et}</span>`).join(' ')}
      </div>
      <div class="d-flex justify-content-between align-items-center">
        <div><span class="rating">⭐ 4.5</span></div>
        <div class="fw-bold text-warning">$${producto.precio}</div>
      </div>
      <div class="text-end mt-2">
        <button class="btn btn-reservar" onclick="addToCartFromDOM(this)">Reservar</button>
        ${esAdmin ? `<button class="btn-eliminar ms-2" onclick="eliminarProducto(this)">Eliminar</button>` : ''}
      </div>
    </div>
  `;

  document.getElementById('contenedorTarjetas').appendChild(tarjeta);
}
