from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
from apyori import apriori as apri
plt.style.use('ggplot')


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'database'

mysql = MySQL(app)

# Paginas principales

@app.route('/')
def index(): 
    cursos = ['PHP','C++','Java']
    data = {
        'titulo':'InvestAI | La inteligencia de tus inversiones',
    }
    return render_template('index.html', data=data)

@app.route('/contact')
def contacto():
    data = {
        'titulo':'Contacto',
    }
    return render_template('contact.html', data=data)

@app.route('/addcontact', methods=['POST'])
def addcontact():
    if request.method =='POST' :
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        message = request.form['message']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email, message) VALUES (%s, %s, %s, %s)',(fullname, phone, email, message))
        mysql.connection.commit()
        return render_template('thanks.html')
    


@app.route('/getapri', methods=['GET','POST'])
def getapri():
    data = {
        'titulo':'Reglas de asociación',
    }

    if request.method =='POST' :
        selectapri = request.form['selectapri']
        if(selectapri == "2"):
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM movies')
            df = cur.fetchall()

            DatosMovies = pd.DataFrame(df)
            Transacciones = DatosMovies.values.reshape(-1).tolist()
            Lista = pd.DataFrame(Transacciones)
            Lista['Frecuencia'] = 1
            Lista = Lista.groupby(by=[0], as_index=False).count().sort_values(by=['Frecuencia'], ascending=True) #Conteo
            Lista['Porcentaje'] = (Lista['Frecuencia'] / Lista['Frecuencia'].sum()) #Porcentaje
            Lista = Lista.rename(columns={0 : 'Item'})
            Lista = Lista[ Lista.Item.str.len()>0]
           
            plt.figure(figsize=(16,20), dpi=100)
            plt.title('Grafica de frecuencias')
            plt.ylabel('Item')
            plt.xlabel('Porcentaje de frecuencias')
            plt.barh(Lista['Item'], width=Lista['Porcentaje'], color='#0099ff')
            plt.savefig('app/static/plots/freqplot.png')

            #MoviesLista = DatosMovies.stack().groupby(level=0).apply(list).tolist()
            #ReglasC1 = apri(MoviesLista, min_support=0.01, min_confidence=0.2, min_lift=3)
            #ResultadosC1 = list(ReglasC1)
            #resultados = ""
            #for item in ResultadosC1:
             #   #El primer índice de la lista
              #  Emparejar = item[0]
               # items = [x for x in Emparejar]
                #resultados += str("Regla: " + str(item[0]))

                #El segundo índice de la lista
             #   resultados += str("\nSoporte: " + str(item[1]))

                #El tercer índice de la lista
              #  resultados += str("\nConfianza: " + str(item[2][0][2]))
               # resultados += str("\nElevación: " + str(item[2][0][3])) 
                #resultados += str("\n=====================================") 
            

            #resultado = resultados
            
            return render_template('getapri.html', plot_url ='static/plots/freqplot.png', data=data)
       
    return render_template('apriori.html')


@app.route('/services')
def services():
    data = {
        'titulo':'Servicios',
    }
    return render_template('services.html', data=data)

@app.route('/about')
def about():
    data = {
        'titulo':'Acerca de',
    }
    return render_template('about.html', data=data)



# Algoritmos

@app.route('/apriori')
def apriori():
    data = {
        'titulo':'Reglas de Asociación',
    }
    return render_template('apriori.html', data=data)

@app.route('/distance')
def distance():
    data = {
        'titulo':'Métricas de distancia',
    }
    return render_template('distance.html', data=data)

@app.route('/clustering')
def clustering():
    data = {
        'titulo':'Clustering',
    }
    return render_template('clustering.html', data=data)

@app.route('/logclas')
def logclas():
    data = {
        'titulo':'Clasificación Logística',
    }
    return render_template('logclas.html', data=data)

@app.route('/linearreg')
def linearreg():
    data = {
        'titulo':'Regresión Lineal',
    }
    return render_template('linearreg.html', data=data)

@app.route('/regtree')
def regtree():
    data = {
        'titulo':'Árboles de Regresión',
    }
    return render_template('regtree.html', data=data)



#Error 404

def pagina_no_encontrada(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)