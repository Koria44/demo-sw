# demo-sw // E-commerce NORTE Studio (Streetwear Chile)

Proyecto e-commerce completo de moda urbana y básicos de alto gramaje (**NORTE Studio**), desarrollado con **Django 5.x**, **Tailwind CSS**, **JavaScript Vanilla modular** e ilustraciones vectoriales SVG paramétricas funcionales sin conexión externa.

Todo el contenido visible, mensajes de error, formularios y especificaciones de despacho están adaptados íntegramente al contexto chileno (**es-CL**, moneda CLP con formato `$49.990`, selector de regiones y comunas nacionales, y despacho gratuito sobre `$70.000 CLP`).

---

## 📁 Mapa de Carpetas de demo-sw

```text
demo-sw/
├── manage.py                   # Punto de entrada para comandos administrativos de Django
├── requirements.txt            # Dependencias de Python (Django, django-environ, Pillow, WhiteNoise)
├── package.json                # Configuración de npm y scripts de compilación de Tailwind CSS
├── tailwind.config.js          # Tokens de diseño: paleta streetwear, tipografías y radios de 0-4px
├── .env.example                # Plantilla documentada en español con variables de entorno
├── .env                        # Configuración local activa out-of-the-box
├── .gitignore                  # Exclusiones de Git (entornos virtuales, node_modules, sqlite3, etc.)
├── README.md                   # Documentación técnica completa en español
├── config/                     # Paquete central de configuración de Django
│   ├── settings/
│   │   ├── base.py             # Parámetros compartidos, WhiteNoise y datos de tienda
│   │   ├── dev.py              # Entorno de desarrollo local (DEBUG=True)
│   │   └── prod.py             # Configuración segura para producción (HTTPS, HSTS, cookies)
│   ├── urls.py                 # Enrutador principal, sitemaps XML y manejadores de error 404/500
│   ├── wsgi.py                 # Interfaz WSGI para servidores web
│   └── asgi.py                 # Interfaz ASGI para servidores asíncronos
├── apps/                       # Aplicaciones modulares del proyecto
│   ├── core/                   # Portada, Conócenos, Políticas, Contacto, robots.txt y context processors
│   ├── catalog/                # Categorías, Colecciones, Productos, Variantes, Reseñas y comando seed_demo
│   ├── cart/                   # Motor de carrito en sesión sin login y endpoints JSON para el drawer
│   ├── orders/                 # Checkout simulado con RUT chileno, regiones y confirmación
│   └── newsletter/             # Suscripción por correo con entrega de cupón (10% OFF)
├── templates/                  # Plantillas HTML5 semánticas de Django
│   ├── base.html               # Estructura principal, Open Graph, Twitter Cards y JSON-LD
│   ├── 404.html                # Página de error no encontrado con sugerencias de compra
│   ├── 500.html                # Página de error interno del servidor
│   ├── core/                   # home.html, about.html, policies.html, contact.html
│   ├── catalog/                # product_list.html, product_detail.html, reviews.html
│   ├── cart/                   # cart_detail.html
│   ├── orders/                 # checkout.html, order_success.html
│   └── partials/               # Componentes reutilizables (header, footer, product_card,
│                               # cart_drawer, search_overlay, mobile_menu, garment_svg, review_card)
└── static/                     # Archivos estáticos de frontend
    ├── css/
    │   ├── input.css           # Capas @tailwind, @apply de componentes y keyframes (marquee, shimmer)
    │   └── output.css          # CSS compilado y minificado por el CLI de Tailwind
    ├── js/                     # Módulos JavaScript Vanilla (ES Modules)
    │   ├── main.js             # Orquestador principal y transiciones suaves de página
    │   ├── drawer.js           # Controlador accesible de paneles (Focus Trap, Escape, ARIA)
    │   ├── menu.js             # Panel de navegación para dispositivos móviles
    │   ├── search.js           # Búsqueda en vivo con debounce de 250ms conectada a endpoint JSON
    │   ├── cart.js             # Drawer del carrito, llamadas AJAX, cálculo de envío gratis y rebote
    │   ├── product.js          # Conmutación de color SVG en vivo, selector de tallas y acordeones
    │   └── animations.js       # Revelado de scroll, barra de progreso y rotador de avisos
    └── img/                    # Activos vectoriales (logo.svg, favicon.svg, og-image.svg)
```

---

## 🚀 Instalación y Puesta en Marcha

> **Nota:** Asumimos que ya tienes tu entorno virtual de Python creado y activado en tu terminal.

### 1. Instalar dependencias de Python
```bash
pip install -r requirements.txt
```

### 2. Instalar dependencias de Node.js (Tailwind CSS)
```bash
npm install
```

### 3. Aplicar migraciones a la base de datos
```bash
python manage.py migrate
```

### 4. Poblar datos de demostración (24 prendas, categorías, tallas y reseñas)
Ejecuta el comando personalizado de management:
```bash
python manage.py seed_demo
```

### 5. Compilar los estilos de Tailwind CSS
El proyecto ya incluye un archivo `static/css/output.css` precompilado. Si realizas cambios en los templates o clases de Tailwind, compila con:
```bash
npm run build
```
O para compilación en caliente durante el desarrollo:
```bash
npm run dev
```

### 6. Iniciar el servidor local de desarrollo
```bash
python manage.py runserver
```

Abre tu navegador en [http://127.0.0.1:8000/](http://127.0.0.1:8000/) para explorar la tienda.

---

## 🛠️ Comandos Útiles

- **Ejecutar suite de pruebas unitarias:**
  ```bash
  python manage.py test apps.cart apps.catalog apps.orders
  ```
- **Crear superusuario para el panel de administración:**
  ```bash
  python manage.py createsuperuser
  ```
  Accede al panel en [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).
- **Verificar integridad del proyecto:**
  ```bash
  python manage.py check
  ```

---

## 🛒 Cómo Funciona el Carrito de Compras

1. **Sesión Anónima:** Los usuarios no requieren registrarse ni iniciar sesión para comprar. Las prendas se persisten en la sesión de Django (`request.session['sw_cart']`).
2. **Selección Obligatoria de Talla:** El sistema valida tanto en el cliente como en el servidor (`apps.cart.views.cart_add`) que se haya seleccionado una talla (`XS, S, M, L, XL, XXL`) antes de añadir al carro. Si el usuario intenta agregar sin elegir, recibe una alerta sutil y focalizada.
3. **Drawer Interactivo:** Al pulsar "Agregar a la Bolsa" o hacer clic en el icono del header, se despliega el drawer lateral accesible (`AccessibleDrawer`) con captura de foco y cierre con la tecla `Escape`.
4. **Barra de Despacho Gratuito Dinámica:** Monitorea en tiempo real el umbral de **$70.000 CLP**:
   - Muestra cuántos pesos faltan para desbloquear el beneficio (ej: *"Te faltan $15.010 para despacho gratis"*).
   - Al superar el monto, la barra se completa al 100% y el costo de despacho cambia a **GRATIS**.
5. **Microanimación del Contador:** El badge numérico del header salta con una animación elástica (`badge-bounce`) cada vez que se modifica la cantidad o se añade una prenda.

---

## 🏷️ Cómo Agregar Nuevos Productos

Puedes agregar y administrar productos fácilmente de dos formas:

### Desde el Panel de Administración de Django
1. Ingresa a `/admin/` con tu superusuario.
2. Ve a la sección **Catálogo de Ropa > Productos > Agregar Producto**.
3. Ingresa el nombre (el slug se autocompleta en español), categoría, precio en CLP, descripción y especificaciones técnicas (gramaje, fit y cuidados).
4. Elige el **Molde vectorial SVG** (`hoodie`, `tee`, `zip`, `knit`, `pants`, `jacket`, `beanie`).
5. En las secciones inferiores tabulares, añade las **Variantes de Color** (nombre y código `#HEX`) y las **Tallas con su Stock disponible**.
6. Guarda los cambios: el producto quedará inmediatamente visible en el catálogo y disponible para compra.

---

## 🖼️ Cómo Reemplazar las Ilustraciones SVG por Fotos Reales

El proyecto cuenta con un sistema de **fallback automático desacoplado**:

1. En el modelo `Product`, los campos `image` e `image_back` son de tipo `ImageField` opcionales.
2. En las plantillas (`product_card.html`, `product_detail.html` y `cart_drawer.html`), la lógica está implementada de la siguiente manera:
   ```html
   {% if product.image %}
     <!-- Fotografía real subida por el administrador -->
     <img src="{{ product.image.url }}" alt="{{ product.name }}">
   {% else %}
     <!-- Ilustración vectorial SVG paramétrica (sin recuadros grises) -->
     {% include "partials/garment_svg.html" with type=product.garment_type color=product.default_color.hex_code %}
   {% endif %}
   ```
3. Para usar fotografías de estudio reales:
   - Sube las imágenes a través del admin en los campos **Fotografía real** y **Fotografía trasera real**.
   - Django comenzará a mostrar tus fotografías automáticamente con la relación de aspecto 4:5 (`aspect-lookbook`), sin necesidad de modificar ni una sola línea de código en las plantillas.

---

## 🎨 Paleta y Tokens de Diseño Streetwear

Definidos en `tailwind.config.js`:
- **Fondo Hueso Editorial:** `#F6F5F2` (`bg-bone`)
- **Superficie Oscura:** `#111111` (`bg-dark`)
- **Colores de Prenda:**
  - Negro Carbón: `#161616`
  - Café Chocolate: `#33261D`
  - Gris Melange: `#B6B5B0`
  - Azul Marino Industrial: `#1E2530`
  - Burdeo Vino: `#4A1525`
  - Rosa Palo Empolvado: `#D9B8B0`
  - Verde Oliva Militar: `#383B2D`
  - Blanco Crudo (Raw Cotton): `#ECE7DE`

---

## 🇨🇱 Envíos y Logística Chilena

- **Couriers Soportados:** Blue Express, Starken y Chilexpress.
- **Tiempos de Entrega:** 24-48 horas en la Región Metropolitana, 2-4 días hábiles en regiones.
- **Medios de Pago Simulados:** Webpay Plus (Transbank), Mercado Pago y Transferencia Bancaria Directa.
- **RUT Chileno:** Formulario con limpieza y validación de formato (ej: `12.345.678-9`).
