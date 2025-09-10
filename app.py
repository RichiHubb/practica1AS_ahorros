# python.exe -m venv .venv
# cd .venv/Scripts
# activate.bat
# py -m ensurepip --upgrade
# pip install -r requirements.txt

from flask import Flask

from flask import render_template
from flask import request
from flask import jsonify, make_response

import mysql.connector

import datetime
import pytz

from flask_cors import CORS, cross_origin

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_23005210_bd",
    user="u760464709_23005210_usr",
    password="~3qAQp|V0aD"
)

app = Flask(__name__)
CORS(app)

def pusherProductos():
    import pusher
    
    pusher_client = pusher.Pusher(
      app_id='2046048',
      key='bc1c723155afce8dd187',
      secret='57fd29b7d864a84bf88c',
      cluster='us2',
      ssl=True
    )
    
    pusher_client.trigger("canalProductos", "eventoProductos", {"message": "Hola Mundo!"})
    return make_response(jsonify({}))

def pusherEtiquetas():
    import pusher
    
    pusher_client = pusher.Pusher(
      app_id='2046048',
      key='bc1c723155afce8dd187',
      secret='57fd29b7d864a84bf88c',
      cluster='us2',
      ssl=True
    )

    
    pusher_client.trigger("canalEtiquetas", "eventoEtiquetas", {"message": "Hola World!"})
    return make_response(jsonify({}))

def pusherNotasFinancieras():
    import pusher
    
    pusher_client = pusher.Pusher(
      app_id='2046048',
      key='bc1c723155afce8dd187',
      secret='57fd29b7d864a84bf88c',
      cluster='us2',
      ssl=True
    )
    
    pusher_client.trigger("canalNotasFinancieras", "eventoNotasFinancieras", {"message": "Nueva nota!"})


def pusherCuentas():
    import pusher
    
    pusher_client = pusher.Pusher(
      app_id='2046048',
      key='bc1c723155afce8dd187',
      secret='57fd29b7d864a84bf88c',
      cluster='us2',
      ssl=True
    )

    
    pusher_client.trigger("canalCuentas", "eventoCuentas", {"message": "Hola Mundo!"})
    return make_response(jsonify({}))

def pusherMovimientos():
    import pusher
    pusher_client = pusher.Pusher(
      app_id='2046048',
      key='bc1c723155afce8dd187',
      secret='57fd29b7d864a84bf88c',
      cluster='us2',
      ssl=True
    )
    pusher_client.trigger("canalMovimientos", "eventoMovimientos", {"message": "Nuevo movimiento!"})
    return make_response(jsonify({}))


@app.route("/")
def index():
    if not con.is_connected():
        con.reconnect()

    con.close()

    return render_template("index.html")

@app.route("/app")
def app2():
    if not con.is_connected():
        con.reconnect()

    con.close()

    return render_template("login.html")
    # return "<h5>Hola, soy la view app</h5>"

@app.route("/iniciarSesion", methods=["POST"])
# Usar cuando solo se quiera usar CORS en rutas específicas
# @cross_origin()
def iniciarSesion():
    if not con.is_connected():
        con.reconnect()

    usuario    = request.form["txtUsuario"]
    contrasena = request.form["txtContrasena"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT id
    FROM usuarios

    WHERE nombre = %s
    AND contrasena = %s
    """
    val    = (usuario, contrasena)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/productos")
def productos():
    return render_template("productos.html")

@app.route("/tbodyProductos")
def tbodyProductos():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Producto,
           Nombre_Producto,
           Precio,
           Existencias

    FROM productos

    ORDER BY Id_Producto DESC

    LIMIT 10 OFFSET 0
    """

    cursor.execute(sql)
    registros = cursor.fetchall()

    @app.route("/movimientos")
    def movimientos():
    return render_template("movimientos.html")

    @app.route("/tbodyMovimientos")
    def tbodyMovimientos():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT idMovimiento, monto, fechaHora
    FROM movimientos
    ORDER BY fechaHora DESC
    """
    cursor.execute(sql)
    registros = cursor.fetchall()
    con.close()
    return render_template("tbodyMovimientos.html", movimientos=registros)



    # Si manejas fechas y horas
    """
    for registro in registros:
        fecha_hora = registro["Fecha_Hora"]

        registro["Fecha_Hora"] = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
        registro["Fecha"]      = fecha_hora.strftime("%d/%m/%Y")
        registro["Hora"]       = fecha_hora.strftime("%H:%M:%S")
    """

    con.close()
    return render_template("tbodyProductos.html", productos=registros)

@app.route("/productos/ingredientes/<int:id>")
def productosIngredientes(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT productos.Nombre_Producto, ingredientes.*, productos_ingredientes.Cantidad FROM productos_ingredientes
    INNER JOIN productos ON productos.Id_Producto = productos_ingredientes.Id_Producto
    INNER JOIN ingredientes ON ingredientes.Id_Ingrediente = productos_ingredientes.Id_Ingrediente
    WHERE productos_ingredientes.Id_Producto = %s
    ORDER BY productos.Nombre_Producto
    """

    cursor.execute(sql, (id, ))
    registros = cursor.fetchall()
    con.close()

    return render_template("modal.html", productosIngredientes=registros)

@app.route("/productos/buscar", methods=["GET"])
def buscarProductos():
    if not con.is_connected():
        con.reconnect()

    args     = request.args
    busqueda = args["busqueda"]
    busqueda = f"%{busqueda}%"
    
    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Producto,
           Nombre_Producto,
           Precio,
           Existencias

    FROM productos

    WHERE Nombre_Producto LIKE %s
    OR    Precio          LIKE %s
    OR    Existencias     LIKE %s

    ORDER BY Id_Producto DESC

    LIMIT 10 OFFSET 0
    """
    val    = (busqueda, busqueda, busqueda)

    try:
        cursor.execute(sql, val)
        registros = cursor.fetchall()

        # Si manejas fechas y horas
        """
        for registro in registros:
            fecha_hora = registro["Fecha_Hora"]

            registro["Fecha_Hora"] = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
            registro["Fecha"]      = fecha_hora.strftime("%d/%m/%Y")
            registro["Hora"]       = fecha_hora.strftime("%H:%M:%S")
        """

    except mysql.connector.errors.ProgrammingError as error:
        print(f"Ocurrió un error de programación en MySQL: {error}")
        registros = []

    finally:
        con.close()

    return make_response(jsonify(registros))

@app.route("/producto", methods=["POST"])
# Usar cuando solo se quiera usar CORS en rutas específicas
# @cross_origin()
def guardarProducto():
    if not con.is_connected():
        con.reconnect()

    id          = request.form["id"]
    nombre      = request.form["nombre"]
    precio      = request.form["precio"]
    existencias = request.form["existencias"]
    # fechahora   = datetime.datetime.now(pytz.timezone("America/Matamoros"))
    
    cursor = con.cursor()

    if id:
        sql = """
        UPDATE productos

        SET Nombre_Producto = %s,
            Precio          = %s,
            Existencias     = %s

        WHERE Id_Producto = %s
        """
        val = (nombre, precio, existencias, id)
    else:
        sql = """
        INSERT INTO productos (Nombre_Producto, Precio, Existencias)
                    VALUES    (%s,          %s,      %s)
        """
        val =                 (nombre, precio, existencias)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusherProductos()
    
    return make_response(jsonify({}))

@app.route("/producto/<int:id>")
def editarProducto(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Producto, Nombre_Producto, Precio, Existencias

    FROM productos

    WHERE Id_Producto = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/producto/eliminar", methods=["POST"])
def eliminarProducto():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    DELETE FROM productos
    WHERE Id_Producto = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({}))
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INICIO SECCION CUENTAS
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/cuentas")
def viewCuentas():
    return render_template("cuentas.html")

@app.route("/tbodyCuentas")
def tbodyCuentas():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT id_cuenta,
           nombre,
           balance

    FROM cuentas

    ORDER BY id_cuenta DESC
    """

    cursor.execute(sql)
    registros = cursor.fetchall()
    con.close()

    return render_template("tbodyCuentas.html", cuentas=registros)

@app.route("/cuenta", methods=["POST"])
def guardarCuenta():
    if not con.is_connected():
        con.reconnect()

    nombre      = request.form["nombre"]
    balance      = request.form["balance"]
    
    cursor = con.cursor()

    sql = """
        INSERT INTO cuentas (nombre, balance)
        VALUES    (%s,          %s)
        """
    val = (nombre, balance)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusherCuentas()
    
    return make_response(jsonify({}))

@app.route("/notasFinancieras")
def notasfinancieras():
    return render_template("notasFinancieras.html")

@app.route("/tbodyNotasFinancieras")
def tbodyNotasFinancieras():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT idNota,
           titulo,
           descripcion,
           fechaCreacion

    FROM notasfinancieras

    ORDER BY idNota DESC

    LIMIT 10 OFFSET 0
    """

    cursor.execute(sql)
    registros = cursor.fetchall()

    # Si manejas fechas y horas
   
    for registro in registros:
        fecha_hora = registro["fechaCreacion"]
    if fecha_hora:
        registro["fechaCreacion"] = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
    else:
        registro["fechaCreacion"] = ""

    con.close()
    return render_template("tbodyNotasFinancieras.html", notas=registros)

@app.route("/notafinanciera", methods=["POST"])
def guardarNotaFinanciera():
    if not con.is_connected():
        con.reconnect()

    titulo      = request.form["titulo"]
    descripcion = request.form["descripcion"]
    
    cursor = con.cursor()
    sql = "INSERT INTO notasfinancieras (titulo, descripcion) VALUES (%s, %s)"
    val = (titulo, descripcion)
    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusherNotasFinancieras()

    return make_response(jsonify({}))





# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# FIN SECCION CUENTAS

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Etiquetas
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/etiquetas")
def viewEtiquetas():
    return render_template("etiquetas.html")

@app.route("/tbodyEtiquetas")
def tbodyEtiquetas():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT idEtiqueta,
           nombreEtiqueta

    FROM etiquetas

    ORDER BY idEtiqueta DESC
    """

    cursor.execute(sql)
    registros = cursor.fetchall()
    con.close()

    return render_template("tbodyEtiquetas.html", etiquetas=registros)

@app.route("/etiqueta", methods=["POST"])
# Usar cuando solo se quiera usar CORS en rutas específicas
# @cross_origin()
def guardarEtiqueta():
    if not con.is_connected():
        con.reconnect()

    id          = request.form["id"]
    nombre      = request.form["nombre"]
    
    cursor = con.cursor()

    sql = """
    INSERT INTO productos (nombreEtiqueta)
                VALUES    (%s)
    """
    val = (nombre)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusherEtiquetas()

    return make_response(jsonify({}))










