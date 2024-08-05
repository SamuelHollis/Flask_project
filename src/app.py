from flask import Flask, request, render_template
from pickle import load
import regex as re
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
app = Flask(__name__)
import os

# Obtener el directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construir rutas relativas a partir del directorio actual
model_path = os.path.join(current_dir, "models", "npl_good_42.sav")
vectorizer_path = os.path.join(current_dir, "models", "vectorizer_42.sav")

# Cargar el modelo y el vectorizador usando rutas relativas
model = load(open(model_path, "rb"))
vectorizer = load(open(vectorizer_path, "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    prediction_text = None
    if request.method == "POST":
        # Obtener la URL del formulario
        user_url = request.form["url"]
        def preprocess_text(text):
            # Eliminar prefijo
            text = re.sub(r'^(https?://)?(www\.)?', '', text)
            # Eliminar cualquier caracter que no sea una letra (a-z) o un espacio en blanco ( )
            text = re.sub(r'[^a-z ]', " ", text)
            # Eliminar espacios en blanco
            text = re.sub(r'\s+[a-zA-Z]\s+', " ", text)
            text = re.sub(r'\^[a-zA-Z]\s+', " ", text)
            # Reducir espacios en blanco múltiples a uno único
            text = re.sub(r'\s+', " ", text.lower())
            # Eliminar tags
            text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
            return text
        
        # Llamamos al lematizador
        download('wordnet')
        lemmatizer = WordNetLemmatizer()
        download('stopwords')
        stop_words = stopwords.words('english')
        def lemmatize_text(words, lemmatizer=lemmatizer):
            # lematización
            tokens = [lemmatizer.lemmatize(word) for word in words]
            # sacamos stop words
            tokens = [word for word in tokens if word not in stop_words]
            return tokens
        
        processed_url = preprocess_text(user_url)
        lemmatized_url = lemmatize_text(processed_url.split())
        tokens_list = [' '.join(lemmatized_url)]

        # Asegurarse de que el vectorizador es un objeto TfidfVectorizer
        if not isinstance(vectorizer, TfidfVectorizer):
            raise TypeError("El vectorizador cargado no es un objeto TfidfVectorizer.")
        user_url_vectorized = vectorizer.transform(tokens_list).toarray()

        # Realizar la predicción
        prediction = model.predict(user_url_vectorized)[0]

        # Determinar el resultado
        prediction_text = 'Spam' if prediction == 1 else 'Not Spam'
    return render_template("index.html", prediction=prediction_text)


if __name__ == '__main__':
    app.run(debug=True)