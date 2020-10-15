from flask import Flask, render_template, url_for, request, redirect, make_response
from lang_modele import modelisation, generation_phrases, sample_from_discrete_distrib
from random import sample
import os
from whatsapp_cleanup import whatsapp_clean

UPLOAD_FOLDER = "."
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

modele_lang = {}

@app.route('/')
def hello_world():
    global modele_lang
    modele_lang = {} # réinitialisation du modèle au chargement de la page d'accueil
    return render_template('index.html')

@app.route('/results', methods=["GET","POST"])
def submit_corpus() :
    # https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
    valeur_test = request.form.get("test")
    name = request.form.get("name")
    if request.method == "POST":
        if request.files["file"]:
            # loading file
            uploaded_file = request.files["file"]
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], "corpus.txt"))
        else:
            return "no file"
    with open(os.path.join(app.config['UPLOAD_FOLDER'], "corpus.txt"), 'r') as f:
        file = f.read()
        corpus = whatsapp_clean(file).splitlines()
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "corpus.txt"))
    global modele_lang
    print(modele_lang)
    modele_lang = modelisation(corpus)
    sentence = ' '.join(generation_phrases(modele_lang)).replace('BEGIN NOW ', '').replace(' END', '')

    return render_template("results.html", phrase=sentence)

@app.route('/new', methods=["GET", "POST"])
def generate_new_sentence():
    print(sample_from_discrete_distrib(modele_lang[('BEGIN','NOW')]))
    sentence = ' '.join(generation_phrases(modele_lang)).replace('BEGIN NOW ', '').replace(' END', '')
    return render_template("results.html", phrase=sentence)

@app.route('/sample')
def generate_sample():
    # voir ce thread https://stackoverflow.com/questions/27628053/uploading-and-downloading-files-with-flask
    with open('sample_whatsai.txt', "w") as f:
        f.truncate(0) # on efface le contenu (au cas où)
        for i in range(1, 101):
            sentence = ' '.join(generation_phrases(modele_lang)).replace('BEGIN NOW ', '').replace(' END', '')
            f.write(f"{i:03} {sentence}\n")
    with open('sample_whatsai.txt', "r") as f:
        result = f.read()
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=sample_whatsai.txt"
    return response


if __name__ == '__main__':
    app.run()
