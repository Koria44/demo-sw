"""
Encabezado: Comando de gestión 'seed_demo' para poblar la base de datos de demo-sw.
Crea 6 categorías de streetwear, 2 colecciones/drops, al menos 24 productos con variantes
de color reales, tallas con stock, precios en pesos chilenos (CLP) y reseñas de clientes.
Uso:
    python manage.py seed_demo
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.catalog.models import Category, Collection, Product, ProductColor, ProductSize, Review


class Command(BaseCommand):
    help = 'Puebla la base de datos con datos de demostración para la tienda NORTE Studio (demo-sw).'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando poblamiento de base de datos para NORTE Studio...'))

        with transaction.atomic():
            # 1. Creación de Colecciones / Drops
            drop_invierno, _ = Collection.objects.get_or_create(
                slug='drop-01-invierno-austral',
                defaults={
                    'name': 'Drop 01 - Invierno Austral',
                    'tagline': 'Prendas de alto gramaje para el frío sobrio del hemisferio sur.',
                    'description': 'Lanzamiento inaugural compuesto por frisas pesadas de 450 y 500 GSM, cortes limpios y una paleta inspirada en el hormigón, el asfalto mojado y los tonos tierra.',
                    'is_active': True,
                }
            )

            drop_esenciales, _ = Collection.objects.get_or_create(
                slug='basicos-esenciales',
                defaults={
                    'name': 'Básicos Esenciales',
                    'tagline': 'Siluetas atemporales confeccionadas con algodón peinado de máxima densidad.',
                    'description': 'La base de todo armario streetwear: poleras boxy de 260 GSM y polerones con estructura firme que mantienen su caída lavado tras lavado.',
                    'is_active': True,
                }
            )

            # 2. Creación de Categorías
            categories_data = [
                {
                    'name': 'Hoodies Heavyweight',
                    'slug': 'hoodies',
                    'tagline': 'Capuchas dobles sin cordón, bolsillo canguro oculto y 450 GSM.',
                    'description': 'Nuestra silueta insignia. Hombros caídos y puños acanalados de alta tensión.',
                    'garment_type': 'hoodie',
                    'default_color_hex': '#161616',
                    'order': 1,
                },
                {
                    'name': 'Poleras Boxy Fit',
                    'slug': 'poleras',
                    'tagline': 'Corte cuadrado estructurado en algodón peinado de 260 GSM.',
                    'description': 'Cuellos altos de 3 cm indeformables, mangas amplias hasta el codo y basta recta.',
                    'garment_type': 'tee',
                    'default_color_hex': '#33261D',
                    'order': 2,
                },
                {
                    'name': 'Polerones Zip Up',
                    'slug': 'zip-ups',
                    'tagline': 'Cierres metálicos YKK bidireccionales y calce relajado.',
                    'description': 'Versatilidad para el entretiempo. Felpa perchada pesada con caída relajada.',
                    'garment_type': 'zip',
                    'default_color_hex': '#1E2530',
                    'order': 3,
                },
                {
                    'name': 'Knits & Tejidos',
                    'slug': 'knits',
                    'tagline': 'Tejidos jacquard pesados con textura táctil y lanas suaves.',
                    'description': 'Sweaters con hilado grueso y puntos acanalados inspirados en la arquitectura brutalista.',
                    'garment_type': 'knit',
                    'default_color_hex': '#B6B5B0',
                    'order': 4,
                },
                {
                    'name': 'Pantalones Baggy & Cargo',
                    'slug': 'pantalones',
                    'tagline': 'Pierna ancha, pinzas frontales y gabardina de alta resistencia.',
                    'description': 'Cortes fluidos que descansan perfectamente sobre zapatillas de suela gruesa.',
                    'garment_type': 'pants',
                    'default_color_hex': '#383B2D',
                    'order': 5,
                },
                {
                    'name': 'Chaquetas & Outerwear',
                    'slug': 'chaquetas',
                    'tagline': 'Bombers acolchadas, cueros veganos texturizados y cortavientos.',
                    'description': 'Capas exteriores diseñadas para enfrentar el viento y las noches urbanas frías.',
                    'garment_type': 'jacket',
                    'default_color_hex': '#161616',
                    'order': 6,
                },
            ]

            category_map = {}
            for c_data in categories_data:
                cat, _ = Category.objects.update_or_create(
                    slug=c_data['slug'],
                    defaults=c_data
                )
                category_map[cat.slug] = cat

            # 3. Definición de 24 Productos Streetwear
            products_data = [
                # --- Categoría: Hoodies (4 productos) ---
                {
                    'category': category_map['hoodies'],
                    'collection': drop_invierno,
                    'name': 'Hoodie Heavyweight 450 GSM Negro',
                    'slug': 'hoodie-heavyweight-450-gsm-negro',
                    'subtitle': 'Silueta cuadrada, capucha rígida doble tela y sin cordones',
                    'description': 'Confeccionado en felpa francesa peinada de 450 gramos por metro cuadrado. Proporciona una estructura sólida que no pierde la forma.',
                    'price_clp': 54990,
                    'compare_price_clp': 62990,
                    'fabric_details': '100% Algodón Peruano Peinado 450 GSM',
                    'fit_details': 'Boxy fit, hombros caídos y torso amplio',
                    'garment_type': 'hoodie',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Negro Carbón Lavado', '#161616', 'sw-black', True),
                        ('Gris Melange Claro', '#B6B5B0', 'sw-melange', False),
                        ('Café Chocolate', '#33261D', 'sw-chocolate', False),
                    ]
                },
                {
                    'category': category_map['hoodies'],
                    'collection': drop_invierno,
                    'name': 'Hoodie Washed Chocolate 500 GSM',
                    'slug': 'hoodie-washed-chocolate-500-gsm',
                    'subtitle': 'Tintura en prenda con desgaste sutil en costuras',
                    'description': 'El polerón más pesado de nuestra línea de invierno. Su proceso de garment dye le entrega un tacto suave y un tono café profundo inconfundible.',
                    'price_clp': 59990,
                    'compare_price_clp': None,
                    'fabric_details': '100% Algodón Heavyweight 500 GSM',
                    'fit_details': 'Oversized boxy con basta recogida sutil',
                    'garment_type': 'hoodie',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Café Chocolate Profundo', '#33261D', 'sw-chocolate', True),
                        ('Negro Carbón', '#161616', 'sw-black', False),
                        ('Verde Oliva Deslavado', '#383B2D', 'sw-olive', False),
                    ]
                },
                {
                    'category': category_map['hoodies'],
                    'collection': drop_esenciales,
                    'name': 'Hoodie Esencial Gris Melange 420 GSM',
                    'slug': 'hoodie-esencial-gris-melange',
                    'subtitle': 'Un clásico del sportswear reinterpretado con corte contemporáneo',
                    'description': 'El básico neutro definitivo. Suave al interior con felpa peinada anti-pilling y tejido acanalado 2x2 en puños y pretina.',
                    'price_clp': 49990,
                    'compare_price_clp': None,
                    'fabric_details': '85% Algodón / 15% Poliéster Texturizado 420 GSM',
                    'fit_details': 'Relajado regular-boxy',
                    'garment_type': 'hoodie',
                    'is_featured': False,
                    'is_new': False,
                    'colors': [
                        ('Gris Melange', '#B6B5B0', 'sw-melange', True),
                        ('Azul Marino Industrial', '#1E2530', 'sw-navy', False),
                        ('Blanco Crudo', '#ECE7DE', 'sw-cream', False),
                    ]
                },
                {
                    'category': category_map['hoodies'],
                    'collection': drop_invierno,
                    'name': 'Hoodie Burdeo Vino 450 GSM',
                    'slug': 'hoodie-burdeo-vino-450-gsm',
                    'subtitle': 'Tono burdeo profundo con bordado tonal de isotipo en la manga',
                    'description': 'Color exclusivo de la cápsula de invierno. Capucha con molde envolvente que resguarda del frío sin necesidad de ajustadores.',
                    'price_clp': 56990,
                    'compare_price_clp': 64990,
                    'fabric_details': '100% Algodón Peinado 450 GSM',
                    'fit_details': 'Boxy estructurado',
                    'garment_type': 'hoodie',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Burdeo Vino', '#4A1525', 'sw-burgundy', True),
                        ('Negro Carbón', '#161616', 'sw-black', False),
                    ]
                },

                # --- Categoría: Poleras (4 productos) ---
                {
                    'category': category_map['poleras'],
                    'collection': drop_esenciales,
                    'name': 'Polera Boxy Fit 260 GSM Negra',
                    'slug': 'polera-boxy-fit-260-gsm-negra',
                    'subtitle': 'Cuello alto acanalado de 3 cm y hombro marcadamente caído',
                    'description': 'La camiseta de referencia en nuestra colección. Confeccionada con algodón de 260 GSM que no se trasluce ni pierde rectitud en la caída.',
                    'price_clp': 29990,
                    'compare_price_clp': 34990,
                    'fabric_details': '100% Algodón Peinado Ringspun 260 GSM',
                    'fit_details': 'Boxy cuadrado, manga hasta el pliegue del codo',
                    'garment_type': 'tee',
                    'is_featured': True,
                    'is_new': False,
                    'colors': [
                        ('Negro Carbón', '#161616', 'sw-black', True),
                        ('Blanco Crudo Natural', '#ECE7DE', 'sw-cream', False),
                        ('Gris Melange', '#B6B5B0', 'sw-melange', False),
                    ]
                },
                {
                    'category': category_map['poleras'],
                    'collection': drop_esenciales,
                    'name': 'Polera Raw Cream 260 GSM',
                    'slug': 'polera-raw-cream-260-gsm',
                    'subtitle': 'Algodón sin blanquear con diminutas motas naturales de fibra',
                    'description': 'Tacto orgánico y tonalidad crema sobria. Ideal para vestir bajo camisas abiertas o chaquetas pesadas.',
                    'price_clp': 29990,
                    'compare_price_clp': None,
                    'fabric_details': '100% Algodón Raw 260 GSM',
                    'fit_details': 'Boxy relajado',
                    'garment_type': 'tee',
                    'is_featured': False,
                    'is_new': False,
                    'colors': [
                        ('Blanco Crudo / Raw Cream', '#ECE7DE', 'sw-cream', True),
                        ('Café Chocolate', '#33261D', 'sw-chocolate', False),
                    ]
                },
                {
                    'category': category_map['poleras'],
                    'collection': drop_invierno,
                    'name': 'Polera Boxy Chocolate Profundo',
                    'slug': 'polera-boxy-chocolate-profundo',
                    'subtitle': 'Tinte reactivo de máxima fijación en algodón pesado',
                    'description': 'Aporta calidez cromática a conjuntos monocromáticos oscuros. Excelente densidad y cuello cerrado indeformable.',
                    'price_clp': 31990,
                    'compare_price_clp': None,
                    'fabric_details': '100% Algodón Peinado 260 GSM',
                    'fit_details': 'Boxy con hombro extendido',
                    'garment_type': 'tee',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Café Chocolate', '#33261D', 'sw-chocolate', True),
                        ('Verde Oliva', '#383B2D', 'sw-olive', False),
                        ('Rosa Palo Emborronado', '#D9B8B0', 'sw-rose', False),
                    ]
                },
                {
                    'category': category_map['poleras'],
                    'collection': drop_invierno,
                    'name': 'Polera Dusty Rose 280 GSM Heavyweight',
                    'slug': 'polera-dusty-rose-280-gsm',
                    'subtitle': 'Rosa empolvado lavado en frío con acabado mate',
                    'description': 'Un acento de color refinado que rompe con la sobriedad tradicional sin perder la estética urbana minimalista.',
                    'price_clp': 32990,
                    'compare_price_clp': 38990,
                    'fabric_details': '100% Algodón Compacto 280 GSM',
                    'fit_details': 'Boxy contemporáneo',
                    'garment_type': 'tee',
                    'is_featured': False,
                    'is_new': True,
                    'colors': [
                        ('Rosa Palo Empolvado', '#D9B8B0', 'sw-rose', True),
                        ('Negro Carbón', '#161616', 'sw-black', False),
                    ]
                },

                # --- Categoría: Zip Ups (4 productos) ---
                {
                    'category': category_map['zip-ups'],
                    'collection': drop_invierno,
                    'name': 'Polerón Full Zip Dual Runner Negro',
                    'slug': 'poleron-full-zip-dual-runner-negro',
                    'subtitle': 'Cierre doble deslizador YKK plateado y felpa de 460 GSM',
                    'description': 'Permite abrir el polerón tanto desde el cuello como desde la base para estilizar con pantalones anchos.',
                    'price_clp': 64990,
                    'compare_price_clp': 74990,
                    'fabric_details': '100% Algodón Heavy French Terry 460 GSM',
                    'fit_details': 'Oversized relajado',
                    'garment_type': 'zip',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Negro Carbón', '#161616', 'sw-black', True),
                        ('Azul Marino Industrial', '#1E2530', 'sw-navy', False),
                    ]
                },
                {
                    'category': category_map['zip-ups'],
                    'collection': drop_invierno,
                    'name': 'Zip Up Navy Industrial 450 GSM',
                    'slug': 'zip-up-navy-industrial-450-gsm',
                    'subtitle': 'Color azul noche sobrio con tirador metálico grabado',
                    'description': 'Bolsillos frontales integrados en las costuras laterales para una línea limpia sin abultamientos.',
                    'price_clp': 62990,
                    'compare_price_clp': None,
                    'fabric_details': '100% Algodón Peinado 450 GSM',
                    'fit_details': 'Boxy con caída recta',
                    'garment_type': 'zip',
                    'is_featured': False,
                    'is_new': True,
                    'colors': [
                        ('Azul Marino Industrial', '#1E2530', 'sw-navy', True),
                        ('Gris Melange', '#B6B5B0', 'sw-melange', False),
                    ]
                },
                {
                    'category': category_map['zip-ups'],
                    'collection': drop_esenciales,
                    'name': 'Fleece Zip Up Melange 400 GSM',
                    'slug': 'fleece-zip-up-melange-400-gsm',
                    'subtitle': 'Felpa perchada térmica de máxima suavidad interior',
                    'description': 'Prenda pensada para capas intermedias durante los meses fríos en la zona central y sur de Chile.',
                    'price_clp': 58990,
                    'compare_price_clp': None,
                    'fabric_details': '90% Algodón / 10% Poliéster 400 GSM',
                    'fit_details': 'Regular fit contemporáneo',
                    'garment_type': 'zip',
                    'is_featured': False,
                    'is_new': False,
                    'colors': [
                        ('Gris Melange', '#B6B5B0', 'sw-melange', True),
                        ('Negro Carbón', '#161616', 'sw-black', False),
                    ]
                },
                {
                    'category': category_map['zip-ups'],
                    'collection': drop_invierno,
                    'name': 'Zip Up Chocolate Garment Dyed',
                    'slug': 'zip-up-chocolate-garment-dyed',
                    'subtitle': 'Costuras reforzadas de triple puntada y calce amplio',
                    'description': 'Acabado vintage único obtenido mediante lavado con piedra pómez y enzimas ecológicas.',
                    'price_clp': 65990,
                    'compare_price_clp': 72990,
                    'fabric_details': '100% Algodón Heavyweight 480 GSM',
                    'fit_details': 'Boxy fit sobredimensionado',
                    'garment_type': 'zip',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Café Chocolate', '#33261D', 'sw-chocolate', True),
                        ('Verde Oliva', '#383B2D', 'sw-olive', False),
                    ]
                },

                # --- Categoría: Knits (4 productos) ---
                {
                    'category': category_map['knits'],
                    'collection': drop_invierno,
                    'name': 'Sweater Chunky Knit Gris Hormigón',
                    'slug': 'sweater-chunky-knit-gris-hormigon',
                    'subtitle': 'Hilado grueso en punto inglés con textura arquitectónica',
                    'description': 'Inspirado en las geometrías de la arquitectura brutalista. Cuello redondo grueso y hombros de caída fluida.',
                    'price_clp': 69990,
                    'compare_price_clp': 79990,
                    'fabric_details': '70% Lana Merina Suave / 30% Acrílico de Alta Resistencia',
                    'fit_details': 'Oversized con caída pesada natural',
                    'garment_type': 'knit',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Gris Melange Hormigón', '#B6B5B0', 'sw-melange', True),
                        ('Negro Carbón', '#161616', 'sw-black', False),
                        ('Blanco Crudo', '#ECE7DE', 'sw-cream', False),
                    ]
                },
                {
                    'category': category_map['knits'],
                    'collection': drop_invierno,
                    'name': 'Sweater Ribbed Knit Negro Táctico',
                    'slug': 'sweater-ribbed-knit-negro-tactico',
                    'subtitle': 'Tejido acanalado vertical que estiliza la figura y abriga con firmeza',
                    'description': 'Densidad pesada anti-deformación con mangas alargadas que acumulan volumen en los puños.',
                    'price_clp': 67990,
                    'compare_price_clp': None,
                    'fabric_details': '80% Lana / 20% Nylon Estructural',
                    'fit_details': 'Boxy relajado',
                    'garment_type': 'knit',
                    'is_featured': False,
                    'is_new': True,
                    'colors': [
                        ('Negro Carbón', '#161616', 'sw-black', True),
                        ('Café Chocolate', '#33261D', 'sw-chocolate', False),
                    ]
                },
                {
                    'category': category_map['knits'],
                    'collection': drop_invierno,
                    'name': 'Knit Oversized Raw Cream',
                    'slug': 'knit-oversized-raw-cream',
                    'subtitle': 'Tono marfil natural tejido en punto arroz de galga gruesa',
                    'description': 'Calidez visual y táctil para contrastar con pantalones oscuros o chaquetas de cuero.',
                    'price_clp': 72990,
                    'compare_price_clp': 82990,
                    'fabric_details': '100% Hilado Suave Antipicor',
                    'fit_details': 'Oversized con mangas volumétricas',
                    'garment_type': 'knit',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Blanco Crudo / Raw Cream', '#ECE7DE', 'sw-cream', True),
                        ('Verde Oliva Apagado', '#383B2D', 'sw-olive', False),
                    ]
                },
                {
                    'category': category_map['knits'],
                    'collection': drop_invierno,
                    'name': 'Sweater Waffle Knit Olive Militar',
                    'slug': 'sweater-waffle-knit-olive-militar',
                    'subtitle': 'Trama de panal de abeja profunda que atrapa el calor corporal',
                    'description': 'Estética utilitaria sobria con puños de 8 cm y dobladillo reforzado.',
                    'price_clp': 64990,
                    'compare_price_clp': None,
                    'fabric_details': '100% Algodón Tejido Waffle 480 GSM',
                    'fit_details': 'Boxy fit tradicional',
                    'garment_type': 'knit',
                    'is_featured': False,
                    'is_new': True,
                    'colors': [
                        ('Verde Oliva Militar', '#383B2D', 'sw-olive', True),
                        ('Negro Carbón', '#161616', 'sw-black', False),
                    ]
                },

                # --- Categoría: Pantalones (4 productos) ---
                {
                    'category': category_map['pantalones'],
                    'collection': drop_invierno,
                    'name': 'Pantalón Baggy Pleated Negro',
                    'slug': 'pantalon-baggy-pleated-negro',
                    'subtitle': 'Pinzas dobles frontales, tiro medio-alto y basta ancha de 28 cm',
                    'description': 'Combina la sastrería clásica con la amplitud del skate de los años 90. Confeccionado en twill de algodón pesado.',
                    'price_clp': 59990,
                    'compare_price_clp': 69990,
                    'fabric_details': '100% Gabardina de Algodón Twill 380 GSM',
                    'fit_details': 'Baggy fit con caída ancha recta',
                    'garment_type': 'pants',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Negro Carbón', '#161616', 'sw-black', True),
                        ('Café Chocolate', '#33261D', 'sw-chocolate', False),
                        ('Gris Cemento', '#B6B5B0', 'sw-melange', False),
                    ]
                },
                {
                    'category': category_map['pantalones'],
                    'collection': drop_invierno,
                    'name': 'Cargo Pant Utilitario Olive',
                    'slug': 'cargo-pant-utilitario-olive',
                    'subtitle': 'Bolsillos fuelle 3D discretos y cordones ajustables en los tobillos',
                    'description': 'Diseñado para moverte por la ciudad con total libertad. Rodillas articuladas con pliegues técnicos.',
                    'price_clp': 64990,
                    'compare_price_clp': None,
                    'fabric_details': '100% Algodón Ripstop Antidesgarro',
                    'fit_details': 'Relajado con pierna cónica graduable',
                    'garment_type': 'pants',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Verde Oliva Militar', '#383B2D', 'sw-olive', True),
                        ('Negro Carbón', '#161616', 'sw-black', False),
                    ]
                },
                {
                    'category': category_map['pantalones'],
                    'collection': drop_esenciales,
                    'name': 'Pantalón Sweatpants Baggy Melange',
                    'slug': 'pantalon-sweatpants-baggy-melange',
                    'subtitle': 'Buzo pesado de 450 GSM con pretina elástica y cordón interior de algodón plano',
                    'description': 'Comodidad total sin perder porte. Su corte ancho no se adhiere a la pierna, creando un perfil estructurado.',
                    'price_clp': 49990,
                    'compare_price_clp': None,
                    'fabric_details': '100% Felpa Francesa 450 GSM',
                    'fit_details': 'Baggy relajado con elástico suave en tobillos',
                    'garment_type': 'pants',
                    'is_featured': False,
                    'is_new': False,
                    'colors': [
                        ('Gris Melange', '#B6B5B0', 'sw-melange', True),
                        ('Negro Carbón', '#161616', 'sw-black', False),
                    ]
                },
                {
                    'category': category_map['pantalones'],
                    'collection': drop_invierno,
                    'name': 'Pantalón Carpenter Chocolate',
                    'slug': 'pantalon-carpenter-chocolate',
                    'subtitle': 'Detalles de carpintero con pasador de martillo y paneles dobles en rodillas',
                    'description': 'Inspiración laboral clásica adaptada a la estética streetwear contemporánea con tinte café chocolate profundo.',
                    'price_clp': 62990,
                    'compare_price_clp': 69990,
                    'fabric_details': '100% Algodón Canvas Reforzado',
                    'fit_details': 'Recto amplio',
                    'garment_type': 'pants',
                    'is_featured': False,
                    'is_new': True,
                    'colors': [
                        ('Café Chocolate', '#33261D', 'sw-chocolate', True),
                        ('Blanco Crudo', '#ECE7DE', 'sw-cream', False),
                    ]
                },

                # --- Categoría: Chaquetas (4 productos) ---
                {
                    'category': category_map['chaquetas'],
                    'collection': drop_invierno,
                    'name': 'Chaqueta Bomber Boxy Cuero Sintético Negro',
                    'slug': 'chaqueta-bomber-boxy-cuero-sintetico',
                    'subtitle': 'Cuero vegano mate texturizado con forro acolchado térmico',
                    'description': 'La prenda más destacada del Drop 01. Silueta cropped boxy con hombros anchos y cuello clásico doblado.',
                    'price_clp': 89990,
                    'compare_price_clp': 105990,
                    'fabric_details': 'Exterior 100% Poliuretano Grano Fino / Forro Satinado Acolchado',
                    'fit_details': 'Cropped boxy con elástico de pretina',
                    'garment_type': 'jacket',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Negro Carbón Grano Fino', '#161616', 'sw-black', True),
                        ('Café Chocolate Vintage', '#33261D', 'sw-chocolate', False),
                    ]
                },
                {
                    'category': category_map['chaquetas'],
                    'collection': drop_invierno,
                    'name': 'Chaqueta Workwear Canvas Olive',
                    'slug': 'chaqueta-workwear-canvas-olive',
                    'subtitle': 'Cuello de corderoy a contraste y cuatro bolsillos utilitarios frontales',
                    'description': 'Resistente a la abrasión y al viento. Cierre frontal con tapeta protectora y broches a presión metálicos.',
                    'price_clp': 84990,
                    'compare_price_clp': None,
                    'fabric_details': 'Lona de Algodón Pesada 420 GSM / Cuello Pana 100% Algodón',
                    'fit_details': 'Estructurado regular boxy',
                    'garment_type': 'jacket',
                    'is_featured': False,
                    'is_new': True,
                    'colors': [
                        ('Verde Oliva Militar', '#383B2D', 'sw-olive', True),
                        ('Negro Carbón', '#161616', 'sw-black', False),
                    ]
                },
                {
                    'category': category_map['chaquetas'],
                    'collection': drop_invierno,
                    'name': 'Chaqueta Puffer Acolchada Minimal Negra',
                    'slug': 'chaqueta-puffer-acolchada-minimal',
                    'subtitle': 'Relleno térmico ecológico de alta retención sin costuras visibles exteriores',
                    'description': 'Protección total para las noches invernales en Chile. Repelente al agua ligera con cuello alto protector.',
                    'price_clp': 89990,
                    'compare_price_clp': 99990,
                    'fabric_details': '100% Nylon Ripstop Repelente al Agua / Relleno Plumón Sintético',
                    'fit_details': 'Oversized acolchado',
                    'garment_type': 'jacket',
                    'is_featured': True,
                    'is_new': True,
                    'colors': [
                        ('Negro Mate', '#161616', 'sw-black', True),
                        ('Gris Melange Asfalto', '#B6B5B0', 'sw-melange', False),
                    ]
                },
                {
                    'category': category_map['chaquetas'],
                    'collection': drop_esenciales,
                    'name': 'Chaqueta Coach Ligera Navy',
                    'slug': 'chaqueta-coach-ligera-navy',
                    'subtitle': 'Cortavientos urbano con broches esmaltados y cordón en la basta',
                    'description': 'Ideal para usar sobre poleras o hoodies cuando baja el sol. Muy liviana y fácil de empacar en mochila.',
                    'price_clp': 59990,
                    'compare_price_clp': None,
                    'fabric_details': '100% Poliéster Mate Texturizado',
                    'fit_details': 'Boxy relajado',
                    'garment_type': 'jacket',
                    'is_featured': False,
                    'is_new': False,
                    'colors': [
                        ('Azul Marino Industrial', '#1E2530', 'sw-navy', True),
                        ('Negro Carbón', '#161616', 'sw-black', False),
                    ]
                },
            ]

            # 4. Inserción de Productos, Colores, Tallas y Stock
            sizes_list = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
            created_products = []

            for p_info in products_data:
                colors_spec = p_info.pop('colors')
                product, _ = Product.objects.update_or_create(
                    slug=p_info['slug'],
                    defaults=p_info
                )
                created_products.append(product)

                # Colores
                for c_name, c_hex, c_fam, c_def in colors_spec:
                    ProductColor.objects.update_or_create(
                        product=product,
                        name=c_name,
                        defaults={
                            'hex_code': c_hex,
                            'color_family': c_fam,
                            'is_default': c_def,
                        }
                    )

                # Tallas con stock real
                for sz in sizes_list:
                    # Stock variado según talla común
                    stock_qty = 15 if sz in ['M', 'L'] else (8 if sz in ['XS', 'XXL'] else 12)
                    ProductSize.objects.update_or_create(
                        product=product,
                        size=sz,
                        defaults={
                            'stock': stock_qty,
                            'is_active': True,
                        }
                    )

            # 5. Inserción de Reseñas de Clientes Chilenos
            reviews_data = [
                {
                    'product': created_products[0], # Hoodie 450g negro
                    'author_name': 'Matías Valenzuela',
                    'customer_city': 'Providencia, Santiago',
                    'rating': 5,
                    'title': 'El mejor gramaje que he probado en Chile',
                    'comment': 'La capucha queda parada sola sin colgar hacia atrás. El algodón es pesadísimo, se siente la calidad al instante. Mido 1.78 m, pedí talla L y el boxy fit queda perfecto sobre los hombros.',
                    'verified_purchase': True,
                },
                {
                    'product': created_products[0],
                    'author_name': 'Sofía Abarca',
                    'customer_city': 'Viña del Mar',
                    'rating': 5,
                    'title': 'Superó mis expectativas por lejos',
                    'comment': 'Llegó en 2 días por Blue Express. El negro carbón tiene un acabado lavado mate muy sobrio. Lo lavé ya dos veces con agua fría y no encogió nada.',
                    'verified_purchase': True,
                },
                {
                    'product': created_products[1], # Hoodie chocolate
                    'author_name': 'Cristóbal Muñoz',
                    'customer_city': 'Concepción',
                    'rating': 5,
                    'title': '500 GSM reales, abriga una locura',
                    'comment': 'En Concepción el invierno es helado y húmedo; este polerón reemplaza perfectamente una chaqueta ligera. El color chocolate en persona es increíble.',
                    'verified_purchase': True,
                },
                {
                    'product': created_products[4], # Polera 260g negra
                    'author_name': 'Ignacio Paredes',
                    'customer_city': 'Santiago Centro',
                    'rating': 5,
                    'title': 'Cuello indeformable de verdad',
                    'comment': 'Siempre me pasaba que las poleras se deformaban en el cuello tras dos lavados. Esta tiene un rib de 3 cm muy firme y la tela no transparenta nada.',
                    'verified_purchase': True,
                },
                {
                    'product': created_products[8], # Zip Up Dual Runner
                    'author_name': 'Lucas Vera',
                    'customer_city': 'Ñuñoa, Santiago',
                    'rating': 5,
                    'title': 'El cierre doble es un game-changer',
                    'comment': 'Poder abrirlo desde abajo cambia completamente cómo luce cuando andas con pantalones anchos. Vale cada peso.',
                    'verified_purchase': True,
                },
                {
                    'product': created_products[12], # Chunky knit gris
                    'author_name': 'Valentina Silva',
                    'customer_city': 'Valdivia',
                    'rating': 5,
                    'title': 'Textura y caída espectacular',
                    'comment': 'El punto inglés es súper grueso pero no pica en la piel. Me encantó la estética minimalista sin logos gigantes.',
                    'verified_purchase': True,
                },
                {
                    'product': created_products[16], # Pantalón baggy negro
                    'author_name': 'Vicente Morales',
                    'customer_city': 'La Serena',
                    'rating': 5,
                    'title': 'La caída perfecta sobre zapatillas',
                    'comment': 'Las pinzas le dan un look mucho más limpio y formal que un buzo normal, pero con la misma comodidad. Muy recomendado.',
                    'verified_purchase': True,
                },
                {
                    'product': created_products[20], # Bomber cuero sintético
                    'author_name': 'Diego Sepúlveda',
                    'customer_city': 'Las Condes, Santiago',
                    'rating': 5,
                    'title': 'Pieza central de mi clóset',
                    'comment': 'La textura del cuero sintético es mate y no suena plástico al moverse. El forro abriga bastante más de lo que esperaba.',
                    'verified_purchase': True,
                },
            ]

            for r_info in reviews_data:
                Review.objects.get_or_create(
                    product=r_info['product'],
                    author_name=r_info['author_name'],
                    title=r_info['title'],
                    defaults=r_info
                )

        self.stdout.write(self.style.SUCCESS(
            f'¡Poblamiento completado con éxito! Se crearon 6 categorías, 2 colecciones, '
            f'{len(created_products)} productos con colores, tallas y reseñas.'
        ))
