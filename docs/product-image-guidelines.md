# Recomendaciones para previews de imagen en terminal

Esta nota queda como referencia para una futura vista previa con imágenes reales convertidas a bloques ANSI/Unicode. La feature no está implementada todavía.

## Objetivo

Que una imagen de producto siga siendo reconocible al reducirse a una representación de terminal. La conversión a bloques funciona mejor con imágenes preparadas como fichas de producto simples, no con fotografías complejas.

## Características recomendadas

- Producto grande y centrado, ocupando aproximadamente 70-90% del encuadre.
- Fondo simple: blanco, negro, gris sólido o transparente.
- Alto contraste entre el objeto y el fondo.
- Un solo producto por imagen siempre que sea posible.
- Silueta clara y reconocible.
- Iluminación uniforme, sin sombras duras ni reflejos fuertes.
- Imagen fuente limpia de al menos 800x800 o 1024x1024.
- Formato cuadrado o 4:3 para facilitar el recorte.

## Evitar

- Kits completos con muchos componentes pequeños mezclados.
- Fotos sobre escritorios, mesas con cables o fondos con textura.
- Texto pequeño en la imagen como elemento principal de identificación.
- Objetos con colores similares al fondo.
- Imágenes panorámicas o muy recortadas.

## Tamaño sugerido para ANSI

Un preview razonable para TUI debería apuntar a:

```text
40-60 columnas de ancho
16-28 filas de alto
```

Menos resolución visual tiende a volverse abstracta. Más tamaño puede competir con el layout principal.

## Estrategia futura sugerida

Mantener dos assets por producto:

- Imagen real: para abrir con visor externo o una vista gráfica futura.
- Imagen preparada para terminal: recortada, contrastada y simplificada antes de convertirla a bloques.

El inventario podría agregar más adelante un campo como:

```json
{
  "image_path": "assets/products/raspberry-pi-5-kit.jpg",
  "terminal_preview_path": "assets/products/raspberry-pi-5-kit.ansi"
}
```

Para una primera versión portable, conviene que la TUI muestre la ficha técnica y deje la apertura de imagen real a un módulo separado.
