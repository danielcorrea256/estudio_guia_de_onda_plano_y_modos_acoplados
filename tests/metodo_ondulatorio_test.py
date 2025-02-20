import numpy as np
import math
from methods.metodo_ondulatorio import funcion_ondulatoria, metodo_ondulatorio


def test_TE_function(): 
    """
    Verifica que la función funcion_ondulatoria para los modos TE (Transverse Electric) 
    genere resultados consistentes con una funcion hallada anteriormente en el Taller de Fotonica y Fibras opticas.
    Esta funcion es f_TE_reference, y ya se basa en n_co, n_cl, h, k_0 dados

    Se prueba para los tres primeros modos (m = 0, 1, 2).

    Raises:
        AssertionError: Si los valores calculados no coinciden con la referencia.
    """

    # Parámetros de la guía de onda
    n_co = 1.5  # Índice de refracción del núcleo
    n_cl = 1    # Índice de refracción del revestimiento
    h = 1       # Altura del núcleo
    lambd = 1   # Luz incidente
    modo = "TE" # Tipo de modo (Transverse Electric)
    
    # Función que se hallo en el Taller de Fotonica y Fibras opticas
    def f_TE_reference(U, m):
        if m%2 == 0:
            return (U*math.tan(U))**2 + U**2 - 1.25*math.pi**2
        else:
            return (U/math.tan(U))**2 + U**2 - 1.25*math.pi**2        

    # Conjunto de valores en los que vamos a probar la funcion
    # se evita el 0 porque se evalua en cotangente de U
    line = np.linspace(0.001, math.pi/2, 50)

    for m in range(3): 
        # Obtener la función generada por funcion_ondulatoria
        f = funcion_ondulatoria(
            n_co=n_co, 
            n_cl=n_cl, 
            h=h, 
            lambd=lambd,
            m=m, 
            modo=modo
        )

        # Evaluar la función generada y la referencia en el mismo rango
        result = [f(x) for x in line]
        real = [f_TE_reference(x, m) for x in line]

        # Verificar que los resultados sean cercanos
        assert np.allclose(result, real), f"Error en el modo TE m={m}"


def test_TM_function(): 
    """
    Verifica que la función funcion_ondulatoria para los modos TM (Transverse Magnetic) 
    genere resultados consistentes con una funcion hallada anteriormente en el Taller de Fotonica y Fibras opticas.
    Esta funcion es f_TM_reference, y ya se basa en n_co, n_cl, h, k_0 dados

    Se prueba para los tres primeros modos (m = 0, 1, 2).

    Raises:
        AssertionError: Si los valores calculados no coinciden con la referencia.
    """

    # Parámetros de la guía de onda
    n_co = 1.5  # Índice de refracción del núcleo
    n_cl = 1    # Índice de refracción del revestimiento
    h = 1       # Altura del núcleo
    modo = "TM" # Tipo de modo (Transverse Magnetic)
    lambd = 1   # Luz incidente

    # Función que se hallo en el Taller de Fotonica y Fibras opticas
    def f_TM_reference(U, m):
        if m%2 == 0:
            return ((n_cl/n_co)**2 * U*math.tan(U))**2 + U**2 - 1.25*math.pi**2
        else:
            return ((n_cl/n_co)**2 * U/math.tan(U))**2 + U**2 - 1.25*math.pi**2        

    # Conjunto de valores en los que vamos a probar la funcion
    # se evita el 0 porque se evalua en cotangente de U
    line = np.linspace(0.001, math.pi/2, 50)

    for m in range(3):
        # Obtener la función generada por funcion_ondulatoria
        f = funcion_ondulatoria(
            n_co=n_co, 
            n_cl=n_cl, 
            h=h, 
            lambd=lambd, 
            m=m, 
            modo=modo
        )

        # Evaluar la función generada y la referencia en el mismo rango
        result = [f(x) for x in line]
        real = [f_TM_reference(x, m) for x in line]

        # Verificar que los resultados sean cercanos
        assert np.allclose(result, real), f"Error en el modo TM m={m}"


def test_result():
    """
    Prueba la función metodo_ondulatorio verificando que los valores obtenidos 
    para los modos TE y TM sean cercanos a los valores de referencia.

    La prueba compara los resultados calculados con valores de referencia 
    para tres modos de propagación en una guía de onda plana.

    Valores esperados:
        - Modos TE: [75, 59.5, 43.8] grados
        - Modos TM: [72.9, 55.5, 42.5] grados

    Se utiliza una tolerancia de 0.1 a los valores de referencia
    
    Raises:
        AssertionError: Si alguno de los valores calculados difieren por mas de 0.1 de los valores esperados.
    """

    # Valores de referencia obtenidos previamente
    real_values_TE = [75, 59.5, 43.8]
    real_values_TM = [72.9, 55.5, 42.5]

    # Ejecutar el método para calcular los ángulos de los modos TE y TM
    result = metodo_ondulatorio(
        n_co=1.5, 
        n_cl=1,
        h=1,
        lambd=1,
        ms=range(3) 
    )

    # Extraer los valores de TE y compararlos con los valores esperados
    result_TE_array = list(result['TE'].values())
    print("resultados py TE", result_TE_array)
    assert np.allclose(result_TE_array,real_values_TE, atol=0.1), f"Error test result en el modo TE"

    # Extraer los valores de TM y compararlos con los valores esperados
    result_TM_array = list(result['TM'].values())
    print("resultados py TM", result_TM_array)
    assert np.allclose(result_TM_array, real_values_TM, atol=0.1), f"Error test result en el modo TM"