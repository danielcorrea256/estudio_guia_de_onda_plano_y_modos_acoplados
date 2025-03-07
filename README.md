<img src="logo.png" alt="Project Logo" width="200" align="center" />

# Proyecto Estudio Guía de Onda Plano y Modos Acoplados

[![Run Pytest](https://github.com/danielcorrea256/estudio_guia_de_onda_plano_y_modos_acoplados/actions/workflows/tests.yml/badge.svg)](https://github.com/danielcorrea256/estudio_guia_de_onda_plano_y_modos_acoplados/actions/workflows/tests.yml)

## Descripción

Esta aplicación calcula los modos de propagación en una guía de onda plana utilizando dos métodos de análisis complementarios:

- **Método de Rayos**: Analiza la guía de onda utilizando conceptos de óptica geométrica.
- **Método de Análisis de Ondas**: Utiliza teoría de ondas para resolver los modos de propagación.

Para abordar las ecuaciones trascendentales que surgen en ambos métodos, la aplicación implementa el **método numérico de bisección**, una técnica robusta para encontrar soluciones cuando los métodos analíticos no son viables. Una vez determinados los modos, se calculan automáticamente otros parámetros clave de la guía de onda.

## Características

- **Análisis Dual**: Implementa tanto la teoría de rayos como la teoría de ondas para un análisis completo de la guía de onda.
- **Interfaz Gráfica (GUI)**: Desarrollada con **PySide6** para una experiencia de usuario intuitiva.
- **Pruebas Automatizadas**: Se incluyen pruebas con **Pytest** para garantizar fiabilidad.

## Descargas

Descarga la última versión ejecutable:

- **[Versión para Mac OS](https://github.com/danielcorrea256/estudio_guia_de_onda_plano_y_modos_acoplados/releases/latest)**  

## Instalación

### Versión de Desarrollo

Asegúrate de tener **Python 3** instalado en tu sistema.

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/danielcorrea256/estudio_guia_de_onda_plano_y_modos_acoplados.git
   cd estudio_guia_de_onda_plano_y_modos_acoplados
   ```

2. **Crea un entorno virtual (Recomendado):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate
   ```

3. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución de la Aplicación

Para ejecutar la aplicación, usa el siguiente comando:

```bash
python3 main.py
```

La interfaz gráfica se abrirá, permitiéndote seleccionar métodos de análisis y visualizar los resultados.

## Pruebas

Este proyecto incluye pruebas para validar su funcionalidad usando **Pytest**. Ejecuta las pruebas con:

```bash
pytest
```

## Información Adicional

- **Interfaz Gráfica**: La aplicación usa **PySide6** para su interfaz.
- **Métodos Numéricos**: Se emplea el método de bisección para resolver ecuaciones trascendentales.
- **Contribuciones y Problemas**: Si deseas contribuir o reportar problemas, puedes hacer un fork del repositorio, enviar pull requests o abrir un issue.
- **Documentación**: Para más detalles, consulta la [documentación del proyecto](documentation.pdf).

---

¡Disfruta explorando y analizando los modos de propagación en guías de onda!

