from flask import Flask #importamos la clase flask
from flask import render_template, request, redirect,url_for, flash  #lo necesario para levantar el html
from flaskext.mysql import MySQL    #para comunicacion sql
from datetime import datetime       #Para agregar la fecha de la foto
import os   #nos permite acceder a los archivos
from flask import send_from_directory   #Acceso a las carpetas

app= Flask(__name__)    #creo objeto app de clase flask
app.secret_key="ClaveSecreta"

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'    #indicamos el usuario
app.config['MYSQL_DATABASE_PASSWORD']=''    #indicamos la password
app.config['MYSQL_DATABASE_DB']='trabajofinal'   #nombre de la database
mysql.init_app(app)     #llamamos al metodo init_app de mysql con el objeto de flask como parametro

@app.route('/')
def index():
    sql="SELECT * FROM `trabajofinal`.`socios`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    socios=cursor.fetchall()
    conn.commit()

    return render_template('socios/index.html', socios=socios )

@app.route('/filtros')
def filtros():
    return render_template('socios/filtros.html')

@app.route('/filtrar', methods=['POST'])
def filtrar():
    _deporte=request.form['txtDeporte']
    sql="SELECT * FROM `trabajofinal`.`socios` WHERE `deporte`=%s;"
    datos= (_deporte)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos) # ejecuta la sentencia sql
    socios=cursor.fetchall()
    conn.commit()

    return render_template('socios/filtrar.html', socios=socios)


@app.route('/crear')
def crear():
    return render_template('socios/crear.html')

@app.route('/edit/<int:idsocios>')
def edit(idsocios):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `trabajofinal`.`socios` WHERE idsocios=%s;", (idsocios))
    socios=cursor.fetchall()
    conn.commit()
    return render_template('socios/edit.html', socios=socios)


@app.route('/destroy/<int:idsocios>')
def destroy(idsocios):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM `trabajofinal`.`socios` WHERE idsocios=%s;", (idsocios))
    conn.commit()
    return redirect('/')

@app.route('/update', methods=['POST'])
def update():
    _dni=request.form['txtDNI'] 
    _apellido=request.form['txtApellido'] 
    _nombre=request.form['txtNombre'] 
    _deporte=request.form['txtDeporte']
    idsocios=request.form['txtID']
    sql="UPDATE `trabajofinal`.`socios` SET `dni`=%s, `apellido`=%s, `nombre`=%s, `deporte`=%s WHERE idsocios=%s;"
    datos=(_dni, _apellido,_nombre,_deporte, idsocios) # crea la sentencia sql
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos) # ejecuta la sentencia sql
    conn.commit()

    return redirect('/') # y renderiza index.html

@app.route('/store', methods=['POST']) # cuando el formulario de create.hmtl hace el submit envia los datos a la pagina /store
def storage():
    _dni=request.form['txtDNI'] 
    _apellido=request.form['txtApellido'] 
    _nombre=request.form['txtNombre'] 
    _deporte=request.form['txtDeporte']
    if _dni=='' or _apellido=='' or _nombre=='' or _deporte=='':
        flash('Recuerda llenar todos los datos de los campos')
        return redirect(url_for('crear'))
    sql="INSERT INTO `trabajofinal`.`socios` (`dni`,`apellido`,`nombre`,`deporte`) VALUES (%s,%s,%s,%s);"
    datos=(_dni,_apellido,_nombre,_deporte) # crea la sentencia sql
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos) # ejecuta la sentencia sql
    conn.commit()

    return redirect('/') # y renderiza index.html


if __name__ == '__main__':
    app.run(debug=True)     #Ejecutar el programa en debug
