import os
from flask import Flask, request, redirect, url_for, jsonify, send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = '/home/ubuntu/tadhack/music'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/indexmusic', methods=['POST'])
def index_music():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        print(file)
        if file :
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
    return jsonify({'status':'success'})

@app.route('/music/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("2000"), debug=True)

