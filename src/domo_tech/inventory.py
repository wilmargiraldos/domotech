"""Persistent inventory for the Domo Tech store."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict


class ProductRecord(TypedDict):
    id: int
    name: str
    price: float
    cat: str
    stock: int


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
]


class InventoryStore:
    """JSON-backed product inventory."""

    def __init__(self, path: Path | str = "data/inventory.json"):
        self.path = Path(path)
        self._products: list[ProductRecord] = []
        self.load()

    def load(self) -> list[ProductRecord]:
        if not self.path.exists():
            self._products = [dict(product) for product in DEFAULT_INVENTORY]
            self.save()
            return self.list_products()

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self._products = [self._normalize_product(product) for product in data]
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

    def _normalize_product(self, product: dict) -> ProductRecord:
        return {
            "id": int(product["id"]),
            "name": str(product["name"]),
            "price": float(product["price"]),
            "cat": str(product["cat"]),
            "stock": int(product["stock"]),
        }
