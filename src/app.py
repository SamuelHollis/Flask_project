from flask import Flask, request, render_template
from pickle import load

app = Flask(__name__)
model = load(open(r"C:\Users\samue\OneDrive\Escritorio\Docs\4GeeksAcademy\29a clase-Despliegue_modelos_AI_en_Render.com_usando_Flask\Flask_project\src\decision_tree_regressor_default_42.sav", "rb"))

def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index():
    prediction_text = ""
    if request.method == 'POST':
        # Obtener los datos del formulario
        input_data = [float(request.form['Time']),
                      float(request.form['Amount'])] + [float(request.form[f'V{i}']) for i in range(1, 29)]
        
        # Convertir los datos a un array numpy
        input_data = np.array(input_data).reshape(1, -1)
        
        # Realizar la predicción
        prediction = model.predict(input_data)
        
        # Determinar el resultado
        result = 'Fraudulent' if prediction[0] == 1 else 'Not Fraudulent'
        prediction_text = f'Transaction is {result}'
    
    return render_template('index.html', prediction_text=prediction_text)