"""Persistent inventory for the Domo Tech store."""

from __future__ import annotations

import json
from pathlib import Path
from typing import NotRequired, TypedDict


class ProductRecord(TypedDict):
    id: int
    name: str
    price: float
    cat: str
    stock: int
    description: NotRequired[str]
    features: NotRequired[list[str]]
    specs: NotRequired[dict[str, str]]


DEFAULT_INVENTORY: list[ProductRecord] = [
    {"id": 1, "name": "Raspberry Pi 5 8GB Starter Kit", "price": 149.99, "cat": "Raspberry Pi", "stock": 8},
    {"id": 2, "name": "Raspberry Pi Pico W", "price": 12.50, "cat": "Microcontroladores", "stock": 35},
    {"id": 3, "name": "Arduino Uno R4 WiFi", "price": 29.99, "cat": "Arduino", "stock": 18},
    {"id": 4, "name": "Arduino Nano ESP32", "price": 24.90, "cat": "Arduino", "stock": 22},
    {"id": 5, "name": "ESP32 DevKit V1", "price": 10.99, "cat": "Microcontroladores", "stock": 40},
    {"id": 6, "name": "ESP8266 NodeMCU", "price": 7.99, "cat": "Microcontroladores", "stock": 28},
    {"id": 7, "name": "Kit Sensores 37 en 1", "price": 34.99, "cat": "Sensores", "stock": 14},
    {"id": 8, "name": "Sensor DHT22 Temperatura/Humedad", "price": 8.50, "cat": "Sensores", "stock": 31},
    {"id": 9, "name": "Sensor PIR HC-SR501", "price": 4.25, "cat": "Sensores", "stock": 45},
    {"id": 10, "name": "Sensor Ultrasonido HC-SR04", "price": 3.99, "cat": "Sensores", "stock": 50},
    {"id": 11, "name": "Relay Module 4 Canales 5V", "price": 9.75, "cat": "Domotica", "stock": 20},
    {"id": 12, "name": "Relay Module 8 Canales Optoacoplado", "price": 16.50, "cat": "Domotica", "stock": 12},
    {"id": 13, "name": "Shelly Plus 1 Mini", "price": 18.99, "cat": "Domotica", "stock": 17},
    {"id": 14, "name": "Sonoff Basic R4 WiFi Switch", "price": 11.99, "cat": "Domotica", "stock": 24},
    {"id": 15, "name": "Zigbee USB Coordinator CC2652P", "price": 32.00, "cat": "Zigbee", "stock": 9},
    {"id": 16, "name": "Zigbee Door/Window Sensor", "price": 13.25, "cat": "Zigbee", "stock": 26},
    {"id": 17, "name": "Zigbee Smart Plug 16A", "price": 21.50, "cat": "Zigbee", "stock": 15},
    {"id": 18, "name": "MQTT RGB LED Controller", "price": 19.90, "cat": "Iluminacion", "stock": 11},
    {"id": 19, "name": "Tira LED WS2812B 5m", "price": 27.99, "cat": "Iluminacion", "stock": 13},
    {"id": 20, "name": "Fuente 5V 10A para LEDs", "price": 18.75, "cat": "Energia", "stock": 16},
    {"id": 21, "name": "Modulo Buck LM2596", "price": 3.25, "cat": "Energia", "stock": 60},
    {"id": 22, "name": "Protoboard 830 puntos", "price": 6.99, "cat": "Prototipado", "stock": 38},
    {"id": 23, "name": "Jumpers Dupont 120 piezas", "price": 5.50, "cat": "Prototipado", "stock": 44},
    {"id": 24, "name": "Display OLED 0.96 I2C", "price": 6.75, "cat": "Displays", "stock": 32},
    {"id": 25, "name": "LCD 20x4 I2C", "price": 12.99, "cat": "Displays", "stock": 19},
    {"id": 26, "name": "Camara Raspberry Pi Camera Module 3", "price": 34.00, "cat": "Raspberry Pi", "stock": 7},
    {"id": 27, "name": "HAT PoE+ Raspberry Pi", "price": 28.50, "cat": "Raspberry Pi", "stock": 6},
    {"id": 28, "name": "Servo SG90 Micro", "price": 3.99, "cat": "Actuadores", "stock": 52},
    {"id": 29, "name": "Motor Paso a Paso 28BYJ-48 + ULN2003", "price": 7.25, "cat": "Actuadores", "stock": 29},
    {"id": 30, "name": "Cerradura Electrica 12V", "price": 23.40, "cat": "Domotica", "stock": 10},
    {"id": 31, "name": "Lector RFID RC522", "price": 5.99, "cat": "Acceso", "stock": 25},
    {"id": 32, "name": "NFC Tags NTAG215 Pack x10", "price": 9.90, "cat": "Acceso", "stock": 21},
    {"id": 33, "name": "NFC Tags NTAG215 Pack x20", "price": 19.80, "cat": "Acceso", "stock": 11},
]


DEFAULT_PRODUCT_DETAILS: dict[int, dict[str, object]] = {
    1: {
        "description": "Kit compacto para montar un nodo central de automatización, dashboards y servicios locales.",
        "features": ["Incluye potencia suficiente para Home Assistant", "Ideal para Node-RED, MQTT y paneles web"],
        "specs": {"RAM": "8 GB", "Uso recomendado": "Servidor domótico local", "Conectividad": "WiFi, Bluetooth, Ethernet"},
    },
    2: {
        "description": "Microcontrolador RP2040 con WiFi para sensores remotos y automatizaciones de bajo consumo.",
        "features": ["Programable con MicroPython o C/C++", "Formato pequeño para prototipos embebidos"],
        "specs": {"MCU": "RP2040", "GPIO": "26 pines multifunción", "Conectividad": "WiFi 2.4 GHz"},
    },
    3: {
        "description": "Placa Arduino moderna para aprendizaje, control de actuadores y proyectos conectados.",
        "features": ["WiFi integrado", "Compatible con ecosistema Arduino IDE"],
        "specs": {"Voltaje lógico": "5 V", "Entradas/salidas": "14 digitales, 6 analógicas", "Conectividad": "WiFi, Bluetooth"},
    },
    4: {
        "description": "Arduino compacto con ESP32, útil para IoT, telemetría y prototipos con poco espacio.",
        "features": ["Formato Nano", "Buen equilibrio entre potencia y conectividad"],
        "specs": {"MCU": "ESP32-S3", "Voltaje lógico": "3.3 V", "Conectividad": "WiFi, Bluetooth LE"},
    },
    5: {
        "description": "Placa ESP32 versátil para nodos WiFi, BLE, sensores y controladores de automatización.",
        "features": ["Doble núcleo", "Amplio soporte en Arduino, ESP-IDF y MicroPython"],
        "specs": {"MCU": "ESP32", "Voltaje lógico": "3.3 V", "Conectividad": "WiFi, Bluetooth"},
    },
    6: {
        "description": "Módulo WiFi económico para sensores, relés y automatizaciones sencillas.",
        "features": ["Compatible con Arduino IDE", "Excelente para nodos MQTT básicos"],
        "specs": {"MCU": "ESP8266", "Voltaje lógico": "3.3 V", "Conectividad": "WiFi 2.4 GHz"},
    },
    7: {
        "description": "Colección de sensores para prácticas, prototipos y pruebas rápidas de entradas físicas.",
        "features": ["Incluye sensores ambientales, luz, sonido y movimiento", "Útil para laboratorios de aprendizaje"],
        "specs": {"Cantidad": "37 módulos", "Nivel": "Principiante a intermedio", "Compatibilidad": "Arduino, Raspberry Pi"},
    },
    8: {
        "description": "Sensor digital de temperatura y humedad para monitoreo ambiental en interiores.",
        "features": ["Lectura digital calibrada", "Adecuado para estaciones caseras y domótica"],
        "specs": {"Rango humedad": "0-100 % RH", "Rango temperatura": "-40 a 80 C", "Interfaz": "Digital"},
    },
    9: {
        "description": "Sensor PIR para detectar presencia o movimiento en habitaciones, pasillos y accesos.",
        "features": ["Sensibilidad ajustable", "Salida digital simple"],
        "specs": {"Voltaje": "5-20 V", "Alcance": "Hasta 7 m", "Salida": "Digital"},
    },
    10: {
        "description": "Sensor ultrasónico para medir distancia en robots, depósitos y detección de obstáculos.",
        "features": ["Medición sin contacto", "Muy usado en robótica educativa"],
        "specs": {"Rango": "2-400 cm", "Voltaje": "5 V", "Interfaz": "Trigger/Echo"},
    },
    11: {
        "description": "Módulo de relés para controlar cargas de baja o media potencia desde microcontroladores.",
        "features": ["Cuatro canales independientes", "Apto para automatización de luces y actuadores"],
        "specs": {"Canales": "4", "Bobina": "5 V", "Carga típica": "Hasta 10 A por canal"},
    },
    12: {
        "description": "Tarjeta de ocho relés con aislamiento para tableros de pruebas y control múltiple.",
        "features": ["Ocho salidas con optoacoplador", "Práctico para bancos domóticos"],
        "specs": {"Canales": "8", "Bobina": "5 V", "Aislamiento": "Optoacoplado"},
    },
    13: {
        "description": "Interruptor inteligente compacto para automatizar circuitos detrás de pulsadores o cajas pequeñas.",
        "features": ["Compatible con integración local", "Formato mini para instalaciones discretas"],
        "specs": {"Carga": "Hasta 8 A", "Conectividad": "WiFi, Bluetooth", "Uso": "Luces y cargas pequeñas"},
    },
    14: {
        "description": "Switch WiFi para controlar dispositivos eléctricos desde plataformas domóticas.",
        "features": ["Integrable con firmware alternativo", "Apto para encendido remoto"],
        "specs": {"Carga": "Hasta 10 A", "Conectividad": "WiFi", "Entrada": "100-240 VAC"},
    },
    15: {
        "description": "Coordinador USB Zigbee para redes locales con sensores y actuadores de bajo consumo.",
        "features": ["Base para Zigbee2MQTT", "Antena de buena cobertura"],
        "specs": {"Chip": "CC2652P", "Interfaz": "USB", "Uso": "Coordinador Zigbee"},
    },
    16: {
        "description": "Sensor Zigbee para detectar apertura de puertas, ventanas o gabinetes.",
        "features": ["Bajo consumo", "Útil para seguridad y automatizaciones de entrada"],
        "specs": {"Protocolo": "Zigbee", "Alimentación": "Batería", "Evento": "Apertura/cierre"},
    },
    17: {
        "description": "Enchufe inteligente Zigbee para controlar cargas y medir consumo según integración.",
        "features": ["Control local desde coordinador Zigbee", "Formato compacto"],
        "specs": {"Corriente": "16 A", "Protocolo": "Zigbee", "Uso": "Control de tomacorriente"},
    },
    18: {
        "description": "Controlador RGB pensado para tiras LED integradas con MQTT y automatización local.",
        "features": ["Compatible con escenas de iluminación", "Control por red local"],
        "specs": {"Canales": "RGB", "Control": "MQTT", "Uso": "Tiras LED"},
    },
    19: {
        "description": "Tira LED direccionable para efectos, indicadores visuales y ambientación domótica.",
        "features": ["LEDs direccionables individualmente", "Apta para efectos dinámicos"],
        "specs": {"Longitud": "5 m", "Tipo": "WS2812B", "Voltaje": "5 V"},
    },
    20: {
        "description": "Fuente robusta para alimentar tiras LED, servos y prototipos de 5 V.",
        "features": ["Capacidad para cargas demandantes", "Útil en instalaciones con LEDs"],
        "specs": {"Salida": "5 V", "Corriente": "10 A", "Potencia": "50 W"},
    },
    21: {
        "description": "Convertidor DC-DC step-down para alimentar módulos desde fuentes de mayor voltaje.",
        "features": ["Salida ajustable", "Buen recurso para prototipos alimentados por batería"],
        "specs": {"Entrada": "4-40 V", "Salida": "1.25-37 V", "Tipo": "Buck"},
    },
    22: {
        "description": "Protoboard para montar circuitos sin soldadura durante pruebas y aprendizaje.",
        "features": ["Compatible con jumpers Dupont", "Zona amplia para circuitos medianos"],
        "specs": {"Puntos": "830", "Formato": "Sin soldadura", "Uso": "Prototipado"},
    },
    23: {
        "description": "Set de cables Dupont para conectar placas, sensores y protoboards.",
        "features": ["Incluye variaciones macho y hembra", "Facilita prototipos rápidos"],
        "specs": {"Cantidad": "120 piezas", "Tipo": "Dupont", "Uso": "Conexiones de prototipo"},
    },
    24: {
        "description": "Pantalla OLED pequeña para mostrar estados, lecturas y menús en proyectos embebidos.",
        "features": ["Alto contraste", "Solo requiere dos líneas de comunicación I2C"],
        "specs": {"Tamaño": "0.96 pulg", "Resolución": "128x64", "Interfaz": "I2C"},
    },
    25: {
        "description": "Display LCD de cuatro líneas para paneles de control y visualización de datos.",
        "features": ["Texto claro para interfaces simples", "Adaptador I2C integrado"],
        "specs": {"Formato": "20x4", "Interfaz": "I2C", "Retroiluminación": "Sí"},
    },
    26: {
        "description": "Cámara oficial para visión, monitoreo y proyectos de detección con Raspberry Pi.",
        "features": ["Integración directa con Raspberry Pi", "Útil para timbres, vigilancia y visión artificial"],
        "specs": {"Resolución": "12 MP", "Interfaz": "CSI", "Compatibilidad": "Raspberry Pi"},
    },
    27: {
        "description": "HAT para alimentar Raspberry Pi mediante red Ethernet compatible con PoE+.",
        "features": ["Reduce cableado en instalaciones fijas", "Ideal para nodos de red o cámaras"],
        "specs": {"Estándar": "PoE+", "Interfaz": "GPIO", "Compatibilidad": "Raspberry Pi"},
    },
    28: {
        "description": "Micro servo económico para movimiento simple en cerraduras, compuertas y robots pequeños.",
        "features": ["Ligero y fácil de controlar", "Compatible con PWM"],
        "specs": {"Modelo": "SG90", "Torque": "1.8 kg-cm aprox.", "Control": "PWM"},
    },
    29: {
        "description": "Motor paso a paso con driver para movimientos precisos de baja carga.",
        "features": ["Incluye controlador ULN2003", "Adecuado para mecanismos pequeños"],
        "specs": {"Motor": "28BYJ-48", "Driver": "ULN2003", "Voltaje": "5 V"},
    },
    30: {
        "description": "Cerradura eléctrica para prototipos de control de acceso y puertas automatizadas.",
        "features": ["Accionamiento por 12 V", "Integrable con relé o MOSFET"],
        "specs": {"Voltaje": "12 V", "Uso": "Control de acceso", "Accionamiento": "Electromecánico"},
    },
    31: {
        "description": "Lector RFID para identificación por tarjetas o llaveros en proyectos de acceso.",
        "features": ["Compatible con tarjetas MIFARE", "Comunicación SPI"],
        "specs": {"Modelo": "RC522", "Frecuencia": "13.56 MHz", "Interfaz": "SPI"},
    },
    32: {
        "description": "Paquete de etiquetas NFC para identificación, automatizaciones móviles y pruebas de acceso.",
        "features": ["Regrabables según uso", "Compatibles con muchos teléfonos NFC"],
        "specs": {"Chip": "NTAG215", "Cantidad": "10", "Frecuencia": "13.56 MHz"},
    },
    33: {
        "description": "Paquete ampliado de etiquetas NFC para automatizaciones, inventario y control de acceso.",
        "features": ["Mayor cantidad para despliegues de prueba", "Compatibles con flujos NFC desde móviles"],
        "specs": {"Chip": "NTAG215", "Cantidad": "20", "Frecuencia": "13.56 MHz"},
    },
}


class InventoryStore:
    """JSON-backed product inventory."""

    def __init__(self, path: Path | str = "data/inventory.json"):
        self.path = Path(path)
        self._products: list[ProductRecord] = []
        self.load()

    def load(self) -> list[ProductRecord]:
        if not self.path.exists():
            self._products = [self._normalize_product(product) for product in DEFAULT_INVENTORY]
            self.save()
            return self.list_products()

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        migrated_data = self._merge_default_products(data)
        self._products = [self._normalize_product(product) for product in migrated_data]
        if self._products != data:
            self.save()
        return self.list_products()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self._products, file, indent=2, ensure_ascii=False)
            file.write("\n")

    def list_products(self) -> list[ProductRecord]:
        return [dict(product) for product in self._products]

    def purchase(self, items: dict[int, int]) -> tuple[bool, str]:
        products_by_id = {product["id"]: product for product in self._products}

        for product_id, qty in items.items():
            product = products_by_id.get(product_id)
            if product is None:
                return False, f"PRODUCTO {product_id} NO EXISTE"
            if product["stock"] < qty:
                return False, f"STOCK INSUFICIENTE: {product['name']} ({product['stock']} DISPONIBLES)"

        for product_id, qty in items.items():
            products_by_id[product_id]["stock"] -= qty

        self.save()
        return True, "INVENTARIO ACTUALIZADO"

    def _merge_default_products(self, products: list[dict]) -> list[dict]:
        merged_products = [dict(product) for product in products]
        existing_ids = {int(product["id"]) for product in merged_products}

        for default_product in DEFAULT_INVENTORY:
            if default_product["id"] not in existing_ids:
                merged_products.append(dict(default_product))

        return merged_products

    def _normalize_product(self, product: dict) -> ProductRecord:
        product_id = int(product["id"])
        details = DEFAULT_PRODUCT_DETAILS.get(product_id, {})
        normalized: ProductRecord = {
            "id": int(product["id"]),
            "name": str(product["name"]),
            "price": float(product["price"]),
            "cat": str(product["cat"]),
            "stock": int(product["stock"]),
        }
        description = product.get("description", details.get("description", ""))
        features = product.get("features", details.get("features", []))
        specs = product.get("specs", details.get("specs", {}))
        normalized["description"] = str(description)
        normalized["features"] = [str(feature) for feature in features]
        normalized["specs"] = {str(key): str(value) for key, value in specs.items()}
        return normalized
