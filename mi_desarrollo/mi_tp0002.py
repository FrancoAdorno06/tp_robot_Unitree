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

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO, MISION_LARGA, MISION_SALUDO, MISION_CORRER


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
    if not comando:
        return False

    accion = comando[0]

    if accion in ("detenerse", "saludar"):
        return len(comando) == 1

    if accion in ("avanzar", "girar"):
        if len(comando) != 3:
            return False

        _, velocidad, tiempo = comando

        # bool es subclase de int en Python, asi que lo excluimos
        # a mano para que True/False no cuelen como numeros validos.
        if isinstance(velocidad, bool) or not isinstance(velocidad, (int, float)):
            return False
        if isinstance(tiempo, bool) or not isinstance(tiempo, (int, float)):
            return False

        if tiempo < 0:
            return False

        return True

    # Cualquier otro nombre de comando (por ejemplo "volar") es invalido.
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
    accion = comando[0]

    try:
        if accion == "avanzar":
            _, velocidad, tiempo = comando
            robot.avanzar(velocidad=velocidad, tiempo=tiempo)
            return f"OK: avanzar (velocidad={velocidad}, tiempo={tiempo})"

        elif accion == "girar":
            _, velocidad, tiempo = comando
            robot.girar(velocidad=velocidad, tiempo=tiempo)
            return f"OK: girar (velocidad={velocidad}, tiempo={tiempo})"

        elif accion == "detenerse":
            robot.detenerse()
            return "OK: detenerse"

        elif accion == "saludar":
            robot.saludar()
            return "OK: saludar"

    except ErrorDeSeguridad as error:
        return f"RECHAZADO por el robot: {comando} -> {error}"


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
    for comando in mision:
        if not comando_es_valido(comando):
            historial.append(f"RECHAZADO por formato invalido: {comando}")
            continue

        resultado = ejecutar_comando(robot, comando)
        historial.append(resultado)


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
    exitosos = [linea for linea in historial if linea.startswith("OK")]
    rechazados = [linea for linea in historial if linea.startswith("RECHAZADO")]

    print("=" * 60)
    print("REPORTE DE MISION")
    print("=" * 60)
    print(f"Total de comandos procesados: {len(historial)}")
    print(f"Ejecutados con exito:         {len(exitosos)}")
    print(f"Rechazados:                   {len(rechazados)}")

    if rechazados:
        print("\nMotivos de rechazo:")
        for linea in rechazados:
            print(f"  - {linea}")

    print("=" * 60)


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
        ejecutar_mision(robot, MISION_CON_ERRORES, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
