from flask import Flask, render_template, request, jsonify, send_file
from flask_uploads import UploadSet, configure_uploads, IMAGES
from imutils import paths
from Tester import Tester
import os
from os import system

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        language = request.form.get("language")
        if language == None:
            language = 'en'
        print("Received image :"+filename)
        response = {}
        results= []
        plantResults = Tester.test('static'+os.path.sep+'img'+os.path.sep+filename,'data','data')
        for plantResult in plantResults:
            plant = plantResult.get("class")
            plantProbability = plantResult.get("probability")
            diseaseResults = Tester.test('static'+os.path.sep+'img'+os.path.sep+filename,plant,'data'+os.path.sep+plant)
            print(plant)
            print(plantProbability)
            for diseaseResult in diseaseResults:
                result={}
                result['plant']=plant
                disease=diseaseResult.get("class")
                result['disease']=disease
                result['percentage']="{0:.2f}".format(float(diseaseResult.get("probability"))*100.0*float(plantProbability))
                imageList=list(os.listdir('data'+os.path.sep+plant+os.path.sep+disease))
                imageList.sort()
                imageList=imageList[:3]
                result['images']=imageList
                descfilename = 'description'+os.path.sep+language+os.path.sep+plant+'_'+disease+'.txt'
                descFile = open(descfilename,'r')
                try:
                    result['description']=descFile.read()
                except:
                    result['description']="No description provided" 
                disease=diseaseResult.get("class")
                results.append(result)
        response['results'] = results
        response['filename'] = filename
        print(response)
        return jsonify(response)
    return render_template('upload.html')

@app.route('/image', methods=['GET'])
def downloadImage():
    filename = request.args.get('filename')
    for image in paths.list_images('data'):
        if image.split(os.path.sep)[-1] == filename:
            return send_file(image)
    return "Image file not found"

@app.route('/confirm',methods=['POST'])
def confirmImage():
    if 'photo' in request.files:
        filename = request.form.get('filename')
        plant = request.form.get('plant')
        disease = request.form.get('disease')
        system('cp static'+os.path.sep+'img'+os.path.sep+filename+" dataset"+os.path.sep+plant+os.path.sep+disease+os.path.sep+filename)

if __name__ == '__main__':
    app.run(debug=True)
