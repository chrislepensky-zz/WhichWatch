import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import cPickle as pkl
from single_img_processing import PreprocessPredict

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.model = None


def load_pickle():
    print 'Loading Model...'
    app.model = pkl.load(open('model.pkl', 'rb'))

def predict_watch_type(img):
    return app.model.predict()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html', prediction='This is an example of a casual watch', img_path='static/uploads/audemar.png')


@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    f = request.files['file']

    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        fname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(fname)

        pp = PreprocessPredict(fname, app.model)
        preprocessed = pp.preprocess_vectorize()
        prediction = pp.predict(preprocessed)

        if prediction == 0:
            prediction = 'This is a casual Watch'
        else:
            prediction = 'This is a dress Watch'

        return render_template('index.html', prediction=prediction, img_path=fname)
        

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    load_pickle()
    app.run(host="0.0.0.0", port=6969, debug=True)