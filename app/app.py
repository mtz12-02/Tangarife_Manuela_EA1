
from flask import Flask, request, redirect, url_for
from conexion import obtener_conexion

app = Flask(__name__)


@app.route("/")
def inicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM vehiculos")
    total_vehiculos = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM movimientos WHERE fecha_salida IS NULL"
    )
    vehiculos_parqueados = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM celdas WHERE ocupada = FALSE")
    celdas_disponibles = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT numero
        FROM celdas
        WHERE ocupada = TRUE
        ORDER BY numero
        """
    )
    celdas_ocupadas = cursor.fetchall()

    cursor.execute(
        """
        SELECT placa, marca, modelo, color
        FROM vehiculos
        ORDER BY id_vehiculo DESC
        """
    )
    vehiculos = cursor.fetchall()

    cursor.close()
    conexion.close()

    filas = ""

    filas = ""

    for vehiculo in vehiculos:
        filas += f"""
        <tr>
            <td>{vehiculo[0]}</td>
            <td>{vehiculo[1] or "-"}</td>
            <td>{vehiculo[2] or "-"}</td>
            <td>{vehiculo[3] or "-"}</td>
        </tr>
        """


    ocupadas = ", ".join(celda[0] for celda in celdas_ocupadas)
    if not ocupadas:
        ocupadas = "Ninguna"

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Autos Colombia</title>
    </head>
    <body>
        <h1>Autos Colombia</h1>
        <p>Sistema de gestión de parqueadero</p>

        <h2>Menú principal</h2>
        <p><a href="/registrar">Registrar vehículo</a></p>
        <p><a href="/entrada">Registrar entrada</a></p>
        <p><a href="/salida">Registrar salida</a></p>
        <p><a href="/novedades">Registrar novedad</a></p>
        <p><a href="/historial">Consultar historial</a></p>

        <h2>Resumen del parqueadero</h2>
        <p>Vehículos registrados: {total_vehiculos}</p>
        <p>Vehículos actualmente parqueados: {vehiculos_parqueados}</p>
        <p>Celdas disponibles: {celdas_disponibles}</p>
        <p>Celdas ocupadas: {ocupadas}</p>

        <h2>Vehículos registrados</h2>
        <table border="1" cellpadding="8">
            <tr>
                <th>Placa</th>
                <th>Marca</th>
                <th>Modelo</th>
                <th>Color</th>
            </tr>
            {filas}
        </table>
    </body>
    </html>
    """


@app.route("/registrar", methods=["GET"])
def formulario_registro():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registrar vehículo</title>
    </head>
    <body>
        <h1>Registrar vehículo</h1>

        <form action="/registrar" method="POST">
            <label>Placa:</label>
            <input type="text" name="placa" required maxlength="10">
            <br><br>

            <label>Marca:</label>
            <input type="text" name="marca" maxlength="50">
            <br><br>

            <label>Modelo:</label>
            <input type="text" name="modelo" maxlength="50">
            <br><br>

            <label>Color:</label>
            <input type="text" name="color" maxlength="30">
            <br><br>

            <button type="submit">Guardar vehículo</button>
        </form>

        <p><a href="/">Volver al menú principal</a></p>
    </body>
    </html>
    """


@app.route("/registrar", methods=["POST"])
def registrar():
    placa = request.form["placa"].strip().upper()
    marca = request.form["marca"].strip()
    modelo = request.form["modelo"].strip()
    color = request.form["color"].strip()

    if not placa:
        return "La placa es obligatoria.", 400

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO vehiculos (placa, marca, modelo, color)
            VALUES (%s, %s, %s, %s)
            """,
            (placa, marca or None, modelo or None, color or None)
        )

        conexion.commit()
        cursor.close()
        conexion.close()

        return redirect(url_for("inicio"))

    except Exception:
        return (
            "No se pudo registrar el vehículo. "
            "Comprueba si la placa ya está registrada.",
            400
        )


@app.route("/entrada", methods=["GET", "POST"])
def entrada():
    mensaje = ""

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == "POST":
        try:
            id_vehiculo = int(request.form["id_vehiculo"])

            cursor.execute(
                """
                SELECT id_celda
                FROM celdas
                WHERE ocupada = FALSE
                ORDER BY numero
                LIMIT 1
                """
            )
            celda = cursor.fetchone()

            if celda is None:
                mensaje = "No hay celdas disponibles."

            else:
                id_celda = celda[0]

                cursor.execute(
                    """
                    INSERT INTO movimientos (id_vehiculo, id_celda)
                    VALUES (%s, %s)
                    """,
                    (id_vehiculo, id_celda)
                )

                cursor.execute(
                    """
                    UPDATE celdas
                    SET ocupada = TRUE
                    WHERE id_celda = %s
                    """,
                    (id_celda,)
                )

                conexion.commit()
                mensaje = "Entrada registrada correctamente."

        except Exception:
            conexion.rollback()
            mensaje = (
                "No se pudo registrar la entrada. "
                "Comprueba que el vehículo no esté ya parqueado."
            )

    cursor.execute(
        """
        SELECT id_vehiculo, placa
        FROM vehiculos
        ORDER BY placa
        """
    )
    vehiculos = cursor.fetchall()

    opciones = ""

    for vehiculo in vehiculos:
        opciones += (
            f'<option value="{vehiculo[0]}">'
            f'{vehiculo[1]}</option>'
        )

    cursor.close()
    conexion.close()

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Registrar entrada</title>
    </head>
    <body>
        <h1>Registrar entrada de vehículo</h1>

        <p>{mensaje}</p>

        <form method="POST">
            <label>Selecciona la placa:</label>
            <select name="id_vehiculo" required>
                {opciones}
            </select>

            <button type="submit">Registrar entrada</button>
        </form>

        <p><a href="/">Volver al inicio</a></p>
    </body>
    </html>
    """

@app.route("/salida", methods=["GET", "POST"])
def salida():
    mensaje = ""

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == "POST":
        try:
            id_movimiento = int(request.form["id_movimiento"])

            cursor.execute(
                """
                SELECT id_celda
                FROM movimientos
                WHERE id_movimiento = %s
                  AND fecha_salida IS NULL
                FOR UPDATE
                """,
                (id_movimiento,)
            )
            movimiento = cursor.fetchone()

            if movimiento is None:
                mensaje = "El vehículo ya salió o el movimiento no existe."

            else:
                id_celda = movimiento[0]

                cursor.execute(
                    """
                    UPDATE movimientos
                    SET fecha_salida = CURRENT_TIMESTAMP
                    WHERE id_movimiento = %s
                      AND fecha_salida IS NULL
                    """,
                    (id_movimiento,)
                )

                cursor.execute(
                    """
                    UPDATE celdas
                    SET ocupada = FALSE
                    WHERE id_celda = %s
                    """,
                    (id_celda,)
                )

                conexion.commit()
                mensaje = "Salida registrada correctamente. Celda liberada."

        except Exception:
            conexion.rollback()
            mensaje = "No se pudo registrar la salida."

    cursor.execute(
        """
        SELECT m.id_movimiento, v.placa, c.numero, m.fecha_entrada
        FROM movimientos AS m
        JOIN vehiculos AS v
            ON m.id_vehiculo = v.id_vehiculo
        JOIN celdas AS c
            ON m.id_celda = c.id_celda
        WHERE m.fecha_salida IS NULL
        ORDER BY m.fecha_entrada
        """
    )
    movimientos = cursor.fetchall()

    opciones = ""

    for movimiento in movimientos:
        opciones += (
            f'<option value="{movimiento[0]}">'
            f'Placa: {movimiento[1]} - '
            f'Celda: {movimiento[2]}</option>'
        )

    cursor.close()
    conexion.close()

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Registrar salida</title>
    </head>
    <body>
        <h1>Registrar salida de vehículo</h1>

        <p>{mensaje}</p>

        <form method="POST">
            <label>Vehículo que sale:</label>
            <select name="id_movimiento" required>
                {opciones}
            </select>

            <button type="submit">Registrar salida</button>
        </form>

        <p><a href="/">Volver al inicio</a></p>
    </body>
    </html>
    """

@app.route("/novedades", methods=["GET", "POST"])
def novedades():
    mensaje = ""

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == "POST":
        try:
            id_movimiento = int(request.form["id_movimiento"])
            descripcion = request.form["descripcion"].strip()

            if not descripcion:
                mensaje = "Escribe una descripción de la novedad."
            else:
                cursor.execute(
                    """
                    INSERT INTO novedades (id_movimiento, descripcion)
                    SELECT id_movimiento, %s
                    FROM movimientos
                    WHERE id_movimiento = %s
                      AND fecha_salida IS NULL
                    RETURNING id_novedad
                    """,
                    (descripcion, id_movimiento)
                )

                novedad = cursor.fetchone()

                if novedad is None:
                    mensaje = (
                        "No se encontró una estancia activa "
                        "para ese movimiento."
                    )
                else:
                    conexion.commit()
                    mensaje = "Novedad registrada correctamente."

        except Exception:
            conexion.rollback()
            mensaje = "No se pudo registrar la novedad."

    cursor.execute(
        """
        SELECT m.id_movimiento, v.placa, c.numero
        FROM movimientos AS m
        JOIN vehiculos AS v
            ON m.id_vehiculo = v.id_vehiculo
        JOIN celdas AS c
            ON m.id_celda = c.id_celda
        WHERE m.fecha_salida IS NULL
        ORDER BY m.fecha_entrada
        """
    )
    movimientos = cursor.fetchall()

    opciones = ""

    for movimiento in movimientos:
        opciones += (
            f'<option value="{movimiento[0]}">'
            f'Placa: {movimiento[1]} - '
            f'Celda: {movimiento[2]}</option>'
        )

    cursor.close()
    conexion.close()

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registrar novedad</title>
    </head>
    <body>
        <h1>Registrar novedad</h1>
        <p>{mensaje}</p>

        <form method="POST">
            <label>Vehículo:</label>
            <select name="id_movimiento" required>
                {opciones}
            </select>
            <br><br>

            <label>Descripción:</label>
            <textarea name="descripcion" required maxlength="2000"></textarea>
            <br><br>

            <button type="submit">Guardar novedad</button>
        </form>

        <p><a href="/">Volver al menú principal</a></p>
    </body>
    </html>
    """

@app.route("/historial")
def historial():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            m.id_movimiento,
            v.placa,
            c.numero,
            m.fecha_entrada,
            m.fecha_salida,
            COALESCE(
                STRING_AGG(n.descripcion, ' | ' ORDER BY n.fecha_novedad),
                '-'
            )
        FROM movimientos m
        JOIN vehiculos v
            ON v.id_vehiculo = m.id_vehiculo
        JOIN celdas c
            ON c.id_celda = m.id_celda
        LEFT JOIN novedades n
            ON n.id_movimiento = m.id_movimiento
        GROUP BY
            m.id_movimiento,
            v.placa,
            c.numero,
            m.fecha_entrada,
            m.fecha_salida
        ORDER BY m.fecha_entrada DESC
    """)

    movimientos = cursor.fetchall()

    cursor.close()
    conexion.close()

    filas = ""

    for movimiento in movimientos:
        filas += f"""
        <tr>
            <td>{movimiento[0]}</td>
            <td>{movimiento[1]}</td>
            <td>{movimiento[2]}</td>
            <td>{movimiento[3]}</td>
            <td>{movimiento[4] or "En curso"}</td>
            <td>{movimiento[5] or "-"}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Historial - Autos Colombia</title>
    </head>
    <body>
        <h1>Historial del parqueadero</h1>

        <p>
            Consulta las entradas, salidas y novedades
            registradas en el sistema.
        </p>

        <table border="1" cellpadding="8">
            <tr>
                <th>ID</th>
                <th>Placa</th>
                <th>Celda</th>
                <th>Fecha de entrada</th>
                <th>Fecha de salida</th>
                <th>Novedades</th>
            </tr>
            {filas}
        </table>

        <p><a href="/">Volver al menú principal</a></p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)
