<img src="logo.png" alt="Project Logo" width="200" align="right" />

# Proyecto Estudio Guía de Onda Plano y Modos Acoplados

[![Run Pytest](https://github.com/danielcorrea256/estudio_guia_de_onda_plano_y_modos_acoplados/actions/workflows/tests.yml/badge.svg)](https://github.com/danielcorrea256/estudio_guia_de_onda_plano_y_modos_acoplados/actions/workflows/tests.yml)

## Overview

This application calculates the propagation modes in a planar waveguide using two complementary analysis methods:

- **Ray Method**: Analyzes the waveguide using geometric optics concepts.
- **Wave Analysis Method**: Uses wave theory to solve for propagation modes.

To tackle the transcendental equations arising in both methods, the application implements the **bisection numerical method**—a robust technique for finding solutions where analytical methods fall short. Once the modes are determined, other key parameters of the waveguide are computed automatically.

## Features

- **Dual Analysis**: Implements both ray and wave theories for comprehensive waveguide analysis.
- **Robust Numerical Solver**: Uses the bisection method for accurate numerical solutions.
- **Graphical User Interface (GUI)**: Built with **PySide6** for an intuitive user experience.
- **Automated Testing**: Integrated **Pytest** tests ensure reliability.
- **Multi-Platform Releases**: Now includes a release for Mac OS.

## Releases

Download the latest executable releases:

- **[Mac OS Release](https://github.com/danielcorrea256/estudio_guia_de_onda_plano_y_modos_acoplados/releases/latest)**  
  *(Additional releases for other platforms will be available here.)*

## Installation

### Development Version

Make sure you have **Python 3** installed on your system.

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/danielcorrea256/estudio_guia_de_onda_plano_y_modos_acoplados.git
   cd estudio_guia_de_onda_plano_y_modos_acoplados
   ```

2. **Create a Virtual Environment (Recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Launch the application by executing:

```bash
python3 main.py
```

The GUI will open, allowing you to select analysis methods and view results.

## Running Tests

This project includes tests to validate functionality using **Pytest**. Run the tests with:

```bash
pytest
```

## Additional Information

- **GUI Framework**: This project uses **PySide6** for its graphical interface.
- **Numerical Methods**: The bisection method ensures reliable solutions for transcendental equations.
- **Contributions & Issues**: Feel free to fork the repository, submit pull requests, or open issues if you encounter any problems or have suggestions.

---

Enjoy exploring and analyzing waveguide propagation modes!

