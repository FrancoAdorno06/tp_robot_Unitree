# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  .....................................
#  Comision:           .....................................
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    # TU CODIGO ACA
    if not isinstance(comando, tuple) or len(comando) == 0:
        return False

    nombre = comando[0]

    if nombre == "avanzar" or nombre == "girar":
        if len(comando) != 3:
            return False

        velocidad = comando[1]
        tiempo = comando[2]

        # bool es un tipo numerico en Python, pero no cuenta como dato valido.
        if (not isinstance(velocidad, (int, float))
                or isinstance(velocidad, bool)):
            return False

        if (not isinstance(tiempo, (int, float))
                or isinstance(tiempo, bool)):
            return False

        if tiempo < 0:
            return False

        return True

    if nombre == "detenerse" or nombre == "saludar":
        return len(comando) == 1

    return False



# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    # TU CODIGO ACA
    try:
        nombre = comando[0]

        if nombre == "avanzar":
            robot.avanzar(velocidad=comando[1], tiempo=comando[2])
            return "Comando avanzar ejecutado correctamente."

        if nombre == "girar":
            robot.girar(velocidad=comando[1], tiempo=comando[2])
            return "Comando girar ejecutado correctamente."

        if nombre == "detenerse":
            robot.detenerse()
            return "Comando detenerse ejecutado correctamente."

        if nombre == "saludar":
            robot.saludar()
            return "Comando saludar ejecutado correctamente."

        return "Comando rechazado: nombre de comando desconocido."

    except ErrorDeSeguridad as error:
        return "Comando rechazado por seguridad: " + str(error)
    MISION_BASICA = [
    robot.avanzar("avanzar", 0.2, 2.0),      # 0.2 x 2.0 = 0.4 metros
    robot.girar("girar", -0.5, 3.14),      # -0.5 x 3.14 = -1.57 rad = 90 grados a la derecha
    robot.avanzar("avanzar", 0.2, 2.0),
    robot.detenerse("detenerse"),
]



# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    # TU CODIGO ACA
    for comando in mision:
        if not comando_es_valido(comando):
            historial.append((False, comando, "Comando invalido."))
        else:
            resultado = ejecutar_comando(robot, comando)

            if resultado.startswith("Comando rechazado"):
                historial.append((False, comando, resultado))
            else:
                historial.append((True, comando, resultado))
    


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    # TU CODIGO ACA
    ejecutados = 0
    rechazados = 0

    print("\n===== REPORTE DE LA MISION =====")

    for registro in historial:
        correcto = registro[0]
        comando = registro[1]
        mensaje = registro[2]

        if correcto:
            ejecutados += 1
            print("OK:", comando, "-", mensaje)
        else:
            rechazados += 1
            print("RECHAZADO:", comando, "-", mensaje)

    print("\nComandos ejecutados correctamente:", ejecutados)
    print("Comandos rechazados:", rechazados)


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_BASICA, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
