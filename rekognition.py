import json

# Change photo to the path and filename of your image.
import boto3

photo = 'bezz.jpeg'
def informationDetails(bucketName, fileName):
    client_rekognition = boto3.client('rekognition', 'us-east-1')
    client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])
    for facedetails in response['FaceDetails']:
        outputs = json.dumps(facedetails, indent=4, sort_keys=True)
    return outputs

def celebrityRecognition(bucketName, fileName):
    client=boto3.client('rekognition', 'us-east-1')
    client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])
    for facedetails in response['CelebrityFaces']:
        outputs = json.dumps(facedetails, indent=4, sort_keys=True)
    for facedetails in response['UnrecognizedFaces']:
        outputs = json.dumps(facedetails, indent=4, sort_keys=True)
    return outputs

rekogDetails = informationDetails(bucketName, fileName)
rekogJson = json.loads(rekogDetails)

celebDetails = celebrityRecognition(bucketName, fileName)
celebJson = json.loads(celebDetails)
print(celebJson)






































# client = boto3.client('rekognition')
#
# with open(photo, 'rb') as image:
#     res = client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])
#
# print(res)
#
# for faceDetail in res['FaceDetails']:
#     print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
#               + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
#     print(' The detected face is: '+str(faceDetail['Gender']['Value']))
#
#     print(faceDetail['Emotions'])
#
#
#     # print('Here are the other attributes:')
#     #print(json.dumps(faceDetail, indent=4, sort_keys=True))
