import os
import cv2
import face_recognition
import pickle


def generatePath():
    imgModeList = []
    studentIds = []
    folderPath = 'D:/Projects/facial_recoginition_system/static/Users/images'
    Pathlist = os.listdir(folderPath)


    for path in Pathlist:
        imgModeList.append(cv2.imread(os.path.join(folderPath, path)))
        studentIds.append(os.path.splitext(path)[0])
        fileName = f'{folderPath}/{path}'
        print(fileName)
        print(studentIds)
    return imgModeList, studentIds


def findEncodings(imgList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # It's a good practice to check if any faces are found before accessing the list
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encode = encodes[0]
            encodeList.append(encode)
        else:
            # Handle the case where no faces are detected
            print("No faces found in the image.")
    return encodeList


def main_encoding():
    imgModeList, studentIds = generatePath()
    print("Generating Encoding")
    encodeKnownList = findEncodings(imgModeList)
    if not encodeKnownList:  # Checks if the list is empty
        print("No encodings generated. Exiting.")
        return  # Exit the function if no encodings were generated
    encodeListKnowsWithIds = [encodeKnownList, studentIds]
    print(encodeListKnowsWithIds)
    print("Done Generating Encoding")
    file = open("D:/Projects/facial_recoginition_system/encodings/encodeFile.p", "wb")
    pickle.dump(encodeListKnowsWithIds, file)
    file.close()

