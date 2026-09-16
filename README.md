# 📊 Generador de Organigramas en Python

Una herramienta de Python diseñada para construir, visualizar y exportar organigramas institucionales y empresariales a partir de fuentes de datos estructuradas (archivos CSV, Excel o JSON).

---

## 📌 Características

* 📂 **Carga flexible de datos:** Soporta datos desde CSV, JSON o bases de datos relacionales.
* 🌲 **Estructura jerárquica automática:** Relaciona automáticamente empleados/cargos con sus respectivos supervisores o departamentos.
* 🎨 **Visualización personalizada:** Generación de diagramas de árbol claros y personalizables con colores, niveles y cajas.
* 💾 **Exportación multiformato:** Exporta los organigramas a formatos como PNG, SVG, PDF o HTML interactivo.

---

## 🛠️ Requisitos Previos

Asegúrate de tener instalado Python 3.8 o superior. Dependiendo de la biblioteca elegida para el renderizado, podrías necesitar Graphviz u otras dependencias auxiliares:

```bash
# En sistemas basados en Debian/Ubuntu
sudo apt install graphviz
