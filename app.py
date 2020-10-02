import json
import boto3
from flask import Flask, render_template, request, make_response
from werkzeug.utils import secure_filename

app = Flask(__name__)
bucketName = 'helpmetofindbucketname'


@app.route('/')
def upload_file():
    return render_template('home.html')

def informationDetails(bucketName, fileName):
    client_rekognition = boto3.client('rekognition', 'us-east-1')
    response = client_rekognition.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucketName,
                'Name': fileName
            }
        },
        Attributes=['ALL','DEFAULT']
    )
    for facedetails in response['FaceDetails']:
        outputs = json.dumps(facedetails, indent=4, sort_keys=True)
    return outputs

def celebrityRecognition(bucketName, fileName):
    client=boto3.client('rekognition', 'us-east-1')
    response = client.recognize_celebrities(
        Image={
            'S3Object': {
                'Bucket': bucketName,
                'Name': fileName
            }
        }
    )
    for facedetails in response['CelebrityFaces']:
        outputs = json.dumps(facedetails, indent=4, sort_keys=True)
    for facedetails in response['UnrecognizedFaces']:
        outputs = json.dumps(facedetails, indent=4, sort_keys=True)
    return outputs



@app.route('/analyze', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        photo = request.files['file']

        if photo:
            fileName = secure_filename(photo.filename)
            photo.save(fileName)
            boto_client = boto3.client('s3')

            boto_client.upload_file(fileName, bucketName,fileName)



        rekogDetails = informationDetails(bucketName, fileName)
        rekogJson = json.loads(rekogDetails)

        celebDetails = celebrityRecognition(bucketName, fileName)
        celebJson = json.loads(celebDetails)
        print(celebJson)
        if celebJson['Name'] == 'Jeff Bezos':
            celebrity = celebJson['Name']


        else:
            celebrity = "The person in picture is not celebrity!!! "



        gender = rekogJson['Gender']['Value']
        high = rekogJson['AgeRange']['High']
        low = rekogJson['AgeRange']['Low']

        values = []
        for value in rekogJson['Emotions']:
            values.append(value['Confidence'])
        emotion = rekogJson['Emotions'][values.index(max(values))]['Type']
        emotion = emotion.title()
        eyeGlass = rekogJson['Eyeglasses']['Value']

        img_src = f"https://{bucketName}.s3.amazonaws.com/{fileName}"

        attributes = {
            'image_name':img_src,
            'gender':gender,
            'high':high,
            'low':low,
            'emotion':emotion,
            'eyeGlass':eyeGlass,
            'celebrity':celebrity

        }

        response = render_template('result.html',attributes=attributes)

    return response


if __name__ == '__main__':
    app.run(debug=True)
