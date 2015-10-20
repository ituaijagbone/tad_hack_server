import os, sys, datetime
from flask import Flask, request, redirect, url_for, jsonify, send_from_directory
from werkzeug import secure_filename

from clarify_python import clarify

UPLOAD_FOLDER = '/home/ubuntu/tadhack/music'
HOST_URL = "http://ec2-54-86-44-93.compute-1.amazonaws.com:2000/"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = clarify.Client('')

def send_to_clarify(media_name, media_url):
    client.create_bundle(name=media_name,
        media_url=media_url, notify_url=HOST_URL + 'indexsuccess')

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
            filename = 'l_' + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append({'filename': filename, 'url': HOST_URL + 'music/' + filename})
    
    for item in filenames:
        send_to_clarify(item['filename'], item['url'])

    return jsonify({'status':'success'})

@app.route('/music/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/indextropo', methods=['POST'])
def index_tropo():
    uploaded_files = request.files.getlist("filename")
    filenames = []
    for file in uploaded_files:
        print(file)
        if file :
            filename = 's_' + secure_filename('Journal_' + datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S%p") + ".mp3")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append({'filename': filename, 'url': HOST_URL + 'music/' + filename})

    for item in filenames:
        send_to_clarify(item['filename'], item['url'])
    
    return jsonify({'status':'success'})

@app.route('/callaudio', methods=['POST'])
def call_audio():
    print(request.form)
    return jsonify({'status':'success'})

@app.route('/search', methods=['POST'])
def search_clarify():
    query = request.form['query']
    result = client.search(query=query)
    items = result['_links']['items']
    
    index = 0
    hits = []
    for item in items:
        bundle = client.get_bundle(item['href'])
        print(bundle)
        hits.append(bundle['name'])
        ++index
    
    return jsonify({'result':hits})

@app.route('/journals', methods=['GET'])
def get_journals():
    dirs = os.listdir(UPLOAD_FOLDER)    
    files = [f[2:] for f in dirs if f[:1] == 's']
    count = len(files)
    return jsonify({'count':count, 'files': files})

@app.route('/indexsuccess', methods=['PUT', 'POST'])
def index_success():
    print(request.get_json(force=True))
    return jsonify({'success': 'true'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("2000"), debug=True)

