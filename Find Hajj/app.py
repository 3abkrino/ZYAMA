from flask import Flask, abort
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask import render_template, render_template_string, request



############################################## Configurations ############################################

app = Flask(__name__,template_folder='template')
app.config['DEBUG'] = True

@app.route('/hello')
def helloIndex():
    return render_template('index.html')

@app.route('/api/camera', methods=['POST'])
def cam():
    if not request.json and not 'status' in request.json:
        abort(400)
    
    return jsonify({'res': 'done'}), 200

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True,host='0.0.0.0' )
