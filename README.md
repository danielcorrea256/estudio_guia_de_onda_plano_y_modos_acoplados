# Proyecto Estudio Guía de Onda Plano y Modos Acoplados

[![Run Pytest](https://github.com/danielcorrea256/estudio_guia_de_onda_plano_y_modos_acoplados/actions/workflows/tests.yml/badge.svg)](https://github.com/danielcorrea256/estudio_guia_de_onda_plano_y_modos_acoplados/actions/workflows/tests.yml)

## Description

This application is designed to calculate the propagation modes in a planar waveguide.

The program offers two approaches for analysis:
- The **ray method**
- The **wave analysis method**

To solve the transcendental equations that arise when applying both ray and wave theory, we implement the **bisection numerical method**, allowing us to efficiently and accurately find solutions. This method is fundamental in determining the propagation mode values that cannot be directly obtained analytically. Once the modes are obtained, other key parameters for studying the waveguide are also determined.

## Features
- Implements **ray and wave theory** for waveguide analysis
- Uses the **bisection method** for numerical solutions
- **Graphical User Interface (GUI) with PySide6**
- **Pytest tests included** for validation

## Installation

### Dev Version

Ensure you have **Python 3** installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/danielcorrea256/estudio_guia_de_onda_plano_y_modos_acoplados
   cd estudio_guia_de_onda_plano_y_modos_acoplados
   ```

2. Install dependencies:
> You might want to create an virtual enviroment before this step.
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Simply execute:
```bash
python3 main.py
```

## Running Tests

This project includes **PySide6 tests**. Run the tests using:
```bash
pytest
```

