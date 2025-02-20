import scipy.optimize
import math


def get_W(n_co, n_cl, m, modo):
    """
    En la teoria se tiene W = gamma * h / 2
    Y dependiendo del m y el modo, W se puede expresar como una funcion de U = kappa * h / 2
    Para resolver las ecuaciones vamos a plantear en terminos de U, por lo que necesitaremos tener W como funcion de U

    Args:
        n_co (float): Índice de refracción del núcleo de la guía de onda.
        n_cl (float): Índice de refracción del revestimiento (cladding).
        m (int): Número de modo de propagación (0, 1, 2, ...).
        modo (str): Tipo de modo de propagación, puede ser "TE" (Transverse Electric) o "TM" (Transverse Magnetic)

    Return:
        function: Funcion lambda que representa a W en terminos de U

    Raises:
        ValueError: Si el modo no es "TE" o "TM".
    """

    # De la teoria se tienen los siguientes casos
    if   m%2==0 and modo=="TE":
        return lambda U : U * math.tan(U)
    elif m%2==1 and modo=="TE":
        return lambda U : -U / math.tan(U)
    elif m%2==0 and modo=="TM":
        return lambda U : (n_cl / n_co)**2 * U * math.tan(U)
    elif m%2==1 and modo=="TM":
        return lambda U : -(n_cl / n_co)**2 * U * 1/math.tan(U)
    else:
        raise ValueError(f"Modo no valido, solo se vale TM o TE, se recibio {modo}")


def funcion_ondulatoria(n_co, n_cl, h, lambd, m, modo):
    """
    Retorna una funcion cuyas raices son los valores permitidos para U en la propagacion de modos de onda
    Tenemos en general que debe cumplirse U^2 + W^2 = (k_0 * h / 2)^2 * (n_co^2  - n_cl^2)
    Pero vamos a obtener W en terminos de U, este nuevo termino depende de m y del modo
    Y teniendo la ecuacion en terminos de U, vamos a hallar las raices, que son los valores permitidos 

    Args:
        n_co (float): Índice de refracción del núcleo de la guía de onda.
        n_cl (float): Índice de refracción del revestimiento (cladding).
        h (float): Altura del núcleo de la guía de onda.
        lambd (float): Luz incidente.
        m (int): Número de modo de propagación (0, 1, 2, ...).
        modo (str): Tipo de modo de propagación, puede ser "TE" (Transverse Electric) o "TM" (Transverse Magnetic).

    Returns:
        function: Función lambda donde sus raices son los valores permitidos para U

    Raises:
        ValueError: Si el modo no es "TE" o "TM".
    """

    # W es una funcion en terminos de U.
    W = get_W(
        n_co=n_co, 
        n_cl=n_cl,
        m=m,
        modo=modo
    )

    k_0 = 2*math.pi / lambd

    left_side_equation = lambda U : (U**2 + W(U)**2) 
    right_side_equation = (k_0 * h / 2)**2 * (n_co**2  - n_cl**2)
    
    # Como se tiene de la teoria que left_side_equation = right_side_equation
    # Entonces left_side_equation - right_side_equation = 0.
    z = lambda U : left_side_equation(U) - right_side_equation
    
    # Luego las raices de z son los valores de U permitidos.
    return z


def metodo_ondulatorio(n_co, n_cl, h, lambd, ms):
    """
    
    n_co > n_cl
    agregar n efectivo

    Calcula los ángulos de incidencia permitidos (theta) para los modos TE y TM en una guía de onda
    utilizando el análisis ondulatorio.

    Args:
        n_co (float): Índice de refracción del núcleo de la guía de onda.
        n_cl (float): Índice de refracción del revestimiento (cladding). = nt
        h (float): Altura del núcleo de la guía de onda.
        k_0 (float): Número de onda en el vacío. (k_0 = 2pi / lambda)
        lambd (float): Longitud de onda de la luz en el medio.
        ms (list[int]): Lista de números de modo a calcular.

    Returns:
        dict: Un diccionario con los ángulos de incidencia para los modos TE y TM en grados.
              - 'TE': Diccionario de modos TE con m como clave y theta_m en grados como valor.
              - 'TM': Diccionario de modos TM con m como clave y theta_m en grados como valor.
    """

    TEs = {} # Diccionario para almacenar los ángulos de incidencia para los modos TE
    TMs = {} # Diccionario para almacenar los ángulos de incidencia para los modos TM

    for m in ms:
        # Definir el intervalo de búsqueda para U según la periodicidad de la función tangente
        l = m*math.pi/2 
        r = (m+1)*math.pi/2  
        interval = (l, r) 

        # Resolver para el modo TE
        # 1. Tenemos una expresion f_TE(U) donde al igualar a 0, tenemos los valores de U permitidos
        f_TE = funcion_ondulatoria(n_co, n_cl, h, lambd, m, "TE") 
        
        # 2. Valor valido para U en la ecuacion original
        U_TE = scipy.optimize.root_scalar(f_TE, method="bisect", bracket=interval).root # raiz de f_TE
        
        # 3. Calcular el angulo de incidencia
        theta_TE = math.acos((U_TE * lambd) / (math.pi * n_co)) 
        
        # 4. Guardar el angulo en grados
        TEs[m] = math.degrees(theta_TE) 

        # Resolver para el modo TM, de manera similar al modo TE
        f_TM = funcion_ondulatoria(n_co, n_cl, h, lambd, m, "TM") 
        U_TM = scipy.optimize.root_scalar(f_TM, method="bisect" ,bracket=interval).root 
        theta_TM = math.acos((U_TM * lambd) / (math.pi * n_co))
        TMs[m] = math.degrees(theta_TM)

    # Retornar los ángulos calculados para los modos TE y TM
    return {'TE': TEs, 'TM': TMs}