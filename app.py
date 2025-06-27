from flask import Flask, render_template_string, request, session, jsonify

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  


HTML = """ <!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Viaja a tu manera</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  
  <style>
    body {
      background-color: #f8f9fa;
    }



    .hero {
      background: linear-gradient(to bottom right, #ff7f50, #ff9966);
      color: white;
      padding: 60px 20px 40px;
      text-align: center;
    }

    .hero h1 {
      font-size: 2.2rem;
      font-weight: bold;
    }

    .btn-outline-white {
      border: 2px solid white;
      color: white;
    }

    .btn-outline-white:hover {
      background-color: white;
      color: #ff7f50;
    }

    .filtros button {
      margin: 5px;
    }

    .tarjeta {
      border-radius: 20px;
      overflow: hidden;
      margin-bottom: 30px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
      background: white;
    }

    .tarjeta-header {
      padding: 30px;
      color: white;
    }

    .tarjeta .categoria {
      position: absolute;
      top: 15px;
      left: 15px;
      background: #ffffffcc;
      color: #333;
      font-weight: bold;
      padding: 5px 10px;
      border-radius: 10px;
      font-size: 0.9rem;
    }

    .etiquetas span {
      font-size: 0.8rem;
      margin-right: 5px;
      padding: 4px 8px;
      border-radius: 8px;
    }

    .etiquetas .Individual {
      background: #e0bbf5;
      color: #5a3e8b;
    }

    .etiquetas .Parejas {
      background: #c9daf8;
      color: #2a4d77;
    }

    .etiquetas .Familia {
      background: #d5f5e3;
      color: #2e8b57;
    }

    .etiquetas .Grupos {
      background: #fff4cc;
      color: #8a6d1f;
    }

    .rating {
      color: gold;
      font-weight: bold;
    }

    .btn-reservar {
      background-color: orange;
      color: white;
      border-radius: 10px;
    }
  </style>
</head>
<body>

<!-- Navbar -->
<nav class="navbar navbar-light bg-white border-bottom px-3">
  <div class="container-fluid">
    <span class="navbar-brand text-warning fw-bold">🌐 Versión 2</span>
    <div>
      <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#cartModal">
          🛒
        </button>
      <button class="navbar-toggler" type="button">
        <span class="navbar-toggler-icon"></span>
      </button>
    </div>
  </div>
</nav>

<!-- Hero -->
<section class="hero">
  <h1>Viaja a tu manera</h1>
  <p>Hoteles, autos, paquetes y más. Todo lo que necesitás para tu viaje perfecto.</p>
  <div class="mt-4">
    <button class="btn btn-light me-2">Explorar opciones</button>
    <button class="btn btn-outline-white">Ofertas especiales</button>
  </div>
</section>

<!-- Filtros -->
<section class="container mt-4 filtros text-center">
  <div class="d-flex flex-wrap justify-content-center">
    <button class="btn btn-warning" onclick="filtrar('Todos')">Todos</button>
    <button class="btn btn-outline-secondary" onclick="filtrar('Paquete')">Paquetes</button>
    <button class="btn btn-outline-secondary" onclick="filtrar('Hotel')">Hoteles</button>
    <button class="btn btn-outline-secondary" onclick="filtrar('Auto')">Autos</button>
    <button class="btn btn-outline-secondary" onclick="filtrarEtiqueta('Individual')">Individual</button>
    <button class="btn btn-outline-secondary" onclick="filtrarEtiqueta('Parejas')">Parejas</button>
    <button class="btn btn-outline-secondary" onclick="filtrarEtiqueta('Familia')">Familia</button>
    <button class="btn btn-outline-secondary disabled">Grupos</button>
  </div>
</section>

<!-- Tarjetas -->
<div class="container mt-4" id="contenedorTarjetas">

  <!-- Hotel -->
  <div class="tarjeta position-relative" data-categoria="Hotel" data-etiquetas="Individual Parejas">
    <div class="tarjeta-header" style="background: linear-gradient(to right, #00c6ff, #0072ff);">
      <div class="categoria">Hotel</div>
      <div class="text-center"><img src="https://img.icons8.com/color/96/hotel.png"/></div>
    </div>
    <div class="p-3">
      <h5>Hotel Boutique París</h5>
      <p>Por noche. Ubicación céntrica, desayuno incluido, WiFi gratis.</p>
      <div class="etiquetas mb-2">
        <span class="Individual">Individual</span>
        <span class="Parejas">Parejas</span>
      </div>
      <div class="d-flex justify-content-between align-items-center">
        <div><span class="rating">⭐ 4.7</span> (98)</div>
        <div class="fw-bold text-warning">$199</div>
      </div>
      <div class="text-end mt-2"><button class="btn btn-reservar" onclick="addToCart('Hotel Boutique París', 199)">Reservar</button></div>
    </div>
  </div>

  <!-- Auto -->
  <div class="tarjeta position-relative" data-categoria="Auto" data-etiquetas="Familia Grupos">
    <div class="tarjeta-header" style="background: linear-gradient(to right, #8EC5FC, #E0C3FC);">
      <div class="categoria">Auto</div>
      <div class="text-center"><img src="https://img.icons8.com/color/96/car--v1.png"/></div>
    </div>
    <div class="p-3">
      <h5>SUV Premium</h5>
      <p>Por día. Seguro incluido, kilometraje ilimitado, GPS.</p>
      <div class="etiquetas mb-2">
        <span class="Familia">Familia</span>
        <span class="Grupos">Grupos</span>
      </div>
      <div class="d-flex justify-content-between align-items-center">
        <div><span class="rating">⭐ 4.5</span> (62)</div>
        <div class="fw-bold text-warning">$65</div>
      </div>
      <div class="text-end mt-2"><button class="btn btn-reservar" onclick="addToCart('SUV Premium', 65)">Reservar</button></div>
    </div>
  </div>

  <!-- Paquete -->
  <div class="tarjeta position-relative" data-categoria="Paquete" data-etiquetas="Parejas">
    <div class="tarjeta-header" style="background: linear-gradient(to right, #f6d365, #fda085);">
      <div class="categoria">Paquete</div>
      <div class="text-center"><span style="font-size: 48px;">🏠</span></div>
    </div>
    <div class="p-3">
      <h5>Escapada a la isla</h5>
      <p>Incluye vuelo + hotel. Desayuno, traslados y actividades.</p>
      <div class="etiquetas mb-2">
        <span class="Parejas">Parejas</span>
      </div>
      <div class="d-flex justify-content-between align-items-center">
        <div><span class="rating">⭐ 4.9</span> (34)</div>
        <div class="fw-bold text-warning">$749</div>
      </div>
      <div class="text-end mt-2"><button class="btn btn-reservar" onclick="addToCart('Escapada a la isla', 749)">Reservar</button></div>
    </div>
  </div>

</div>

<section class="py-5 bg-light">
  <div class="container text-center">
    <h2 class="fw-bold mb-5">¿Por qué elegirnos?</h2>
    <div class="row g-4">
      
      <!-- Tarjeta 1 -->
      <div class="col-md-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <div class="mb-3">
              <div class="bg-warning bg-opacity-25 rounded-circle d-inline-flex align-items-center justify-content-center" style="width: 60px; height: 60px;">
                <i class="bi bi-cash-coin fs-3 text-warning"></i>
              </div>
            </div>
            <h5 class="fw-bold">Mejor precio garantizado</h5>
            <p class="text-muted">Si encontrás un precio más bajo, igualamos la oferta y te damos un 10% extra de descuento.</p>
          </div>
        </div>
      </div>

      <!-- Tarjeta 2 -->
      <div class="col-md-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <div class="mb-3">
              <div class="bg-warning bg-opacity-25 rounded-circle d-inline-flex align-items-center justify-content-center" style="width: 60px; height: 60px;">
                <i class="bi bi-shield-check fs-3 text-warning"></i>
              </div>
            </div>
            <h5 class="fw-bold">Reservas seguras</h5>
            <p class="text-muted">Pago seguro, confirmación instantánea y políticas de cancelación flexibles.</p>
          </div>
        </div>
      </div>

      <!-- Tarjeta 3 -->
      <div class="col-md-4">
        <div class="card shadow-sm border-0 h-100 position-relative">
          <div class="card-body">
            <div class="mb-3">
              <div class="bg-warning bg-opacity-25 rounded-circle d-inline-flex align-items-center justify-content-center" style="width: 60px; height: 60px;">
                <i class="bi bi-clock fs-3 text-warning"></i>
              </div>
            </div>
            <h5 class="fw-bold">Atención 24/7</h5>
            <p class="text-muted">Nuestro equipo está disponible todo el día, todos los días, para ayudarte en lo que necesites.</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>
  <div class="modal fade" id="cartModal" tabindex="-1" aria-labelledby="cartModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="cartModalLabel">Tu carrito</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
        </div>
        <div class="modal-body" id="contenidocarrito">
          Cargando carrito...
        </div>
        <div class="modal-footer">
          <button onclick="vaciarCarrito()">Vaciar Carrito</button>
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
          <button type="button" class="btn btn-primary" onclick="checkout()">Finalizar compra</button>
        </div>
      </div>
    </div>
  </div>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

<script>

  function vaciarCarrito() {
  const carrito = document.getElementById('contenidocarrito');
  carrito.innerHTML = '';  
}

  function filtrar(categoria) {
    const tarjetas = document.querySelectorAll('.tarjeta');
    tarjetas.forEach(tarjeta => {
      if (categoria === 'Todos' || tarjeta.dataset.categoria === categoria) {
        tarjeta.style.display = 'block';
      } else {
        tarjeta.style.display = 'none';
      }
    });
  }

  function filtrarEtiqueta(etiqueta) {
    const tarjetas = document.querySelectorAll('.tarjeta');
    tarjetas.forEach(tarjeta => {
      const etiquetas = tarjeta.dataset.etiquetas.split(' ');
      if (etiquetas.includes(etiqueta)) {
        tarjeta.style.display = 'block';
      } else {
        tarjeta.style.display = 'none';
      }
    });
  }

    function addToCart(name, price) {
    $.ajax({
      url: '/add_to_cart',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({name: name, price: price}),
      success: function(response) {
        alert(response.message);
      }
    });
  }

  function loadCart() {
    $.getJSON('/get_cart', function(cart) {
      if(cart.length === 0) {
        $('#cartContent').html('<p>El carrito está vacío.</p>');
      } else {
        let html = '<ul>';
        cart.forEach(item => {
          html += `<li>${item.name} - $${item.price}</li>`;
        });
        html += '</ul>';
        $('#cartContent').html(html);
      }
    });
  }

  var cartModal = document.getElementById('cartModal')
  cartModal.addEventListener('show.bs.modal', loadCart)

  function checkout() {
    alert('Aquí iría la lógica para finalizar la compra');
  }
</script>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
 """

@app.route('/')
def index():
 
    return render_template_string(HTML)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    if not name or price is None:
        return jsonify({'message': 'Datos incompletos'}), 400


    if 'cart' not in session:
        session['cart'] = []

    # Agregar producto
    session['cart'].append({'name': name, 'price': price})
    session.modified = True 

    return jsonify({'message': f'Producto {name} agregado al carrito.'})

@app.route('/get_cart')
def get_cart():
    cart = session.get('cart', [])
    return jsonify(cart)

if __name__ == '__main__':
    app.run(debug=True)
