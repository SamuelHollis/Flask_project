from flask import Flask, request, render_template
from pickle import load

app = Flask(__name__)
model = load(open(r"C:\Users\samue\OneDrive\Escritorio\Docs\4GeeksAcademy\29a clase-Despliegue_modelos_AI_en_Render.com_usando_Flask\Flask_proj_nlp\nlp\src\nlp_42_default.sav", "rb"))

@app.route("/", methods = ["GET", "POST"])
def index():
    prediction_text = None
    if request.method == "POST":
        # Obtener la URL del formulario
        user_url = request.form["url"]
        
        # Procesar la URL (aquí debes incluir cualquier procesamiento necesario que usaste al entrenar tu modelo)
        # Por ejemplo, transformar la URL en una representación adecuada para el modelo
        # input_data = transform(user_url) # Esta es solo una indicación de lo que podrías hacer
        
        # Realizar la predicción
        prediction = model.predict([user_url])[0]
        
        # Determinar el resultado
        prediction_text = 'Spam' if prediction == 1 else 'Not Spam'
    
    return render_template("index.html", prediction=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)