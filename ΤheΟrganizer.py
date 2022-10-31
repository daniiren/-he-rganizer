import os
import sys
import shutil
import time

print("****************************")
print("* Welcome to Τhe Οrganizer *")
print("****************************")

inputPath = input("\nEnter the input path (to read) : ")
inputPath = inputPath.replace("\\", "/") + "/"
outputPath = inputPath

ListOfExtensions = []
ListOfPaths = []
counter = 0
newFoldersNames = []

# Create new folders where names will be named by the files date
def CreateFordersByDate(inputPath) :
    listOfNewForldersNames = []
    for item in os.listdir(inputPath) :
        if (not os.path.isdir(inputPath + item)) :
            dateFormat = time.ctime(os.path.getmtime(inputPath + item))
            month = dateFormat[4:8]
            year = dateFormat[:-5:-1]
            year = year[::-1]
            folderName = month + year
            if (folderName not in listOfNewForldersNames) :
                listOfNewForldersNames.append(folderName)
                os.mkdir(inputPath + folderName)
            os.replace(inputPath + item, inputPath + folderName + "/" + item)
        else :
            CreateFordersByDate(inputPath + item + "/")


# Delete empty folders (for the end of the program)
def DeleteEmptyFolders(inputPath) :
    for item in os.listdir(inputPath) :
        if (os.path.isdir(inputPath + item)) :
            if (len(os.listdir(inputPath + item)) == 0) :
                shutil.rmtree(inputPath + item, ignore_errors = True)
            else :
                DeleteEmptyFolders(inputPath + item + "/")
                if (len(os.listdir(inputPath + item)) == 0) :
                    shutil.rmtree(inputPath + item, ignore_errors = True)


# Finds the extension of every file
def FindFileExtension(item) :
    tempExtension = ""
    for i in range(len(item)-1, 0, -1) :
        if (item[i] == ".") :
            break
        else:
            tempExtension += item[i]
    final = tempExtension[::-1]
    return final.lower()


# Finds the extension (first name) of every folder
def FindFolderExtension(item) :
    startPoint = 0
    final = ""
    for i in range(len(item)-1, 0, -1) :
        if (item[i] == "/") :
            break
        else:
            startPoint += 1
    
    startPoint = len(item) - startPoint
    final = item[startPoint:-6]
    
    return final

# We create the "tempArrayOfLowerFiles" array so we can save in it all the files in the current path but in lower case.
# We do this to avoid possible conflicts between two same names but with different format (upper or lower case),
# because in Windows two name like : "button.png == Button.png" are the same, in python NO!
# Windows : "button.png == Button.png"
# Python  : "button.png != Button.png"
# So in our case we check if a file already exist always with lower case between those two file names (eg "button.png".lower() == "Button.png".lower()).
def checkSameFiles(item, outputPath) :
    tempItem = item
    tempArrayOfLowerFiles = [] 
    
    for currentItem in os.listdir(outputPath) :
        tempArrayOfLowerFiles.append(currentItem.lower())

    while (tempItem.lower() in tempArrayOfLowerFiles) :
        openParentheses = False
        closedParentheses = False
        sameNameCounter = ""
        closedParenthesesIndex = 2
        if ("." in tempItem) :
            fileExtension = FindFileExtension(tempItem)
            for i in range(len(tempItem) - len(fileExtension) - 1, 0, -1) :
                if (openParentheses and tempItem[i] != "(" and not closedParentheses) :
                    sameNameCounter += tempItem[i]
                    closedParenthesesIndex += 1
                if (tempItem[i] == ")") :
                    openParentheses = True
                if (tempItem[i] == "(" and openParentheses) :
                    closedParentheses = True
            sameNameCounter = sameNameCounter[::-1]

            if (openParentheses and closedParentheses) :
                try :
                    sameNameCounter = int(sameNameCounter) + 1
                    tempItem = tempItem[:len(tempItem) - len(fileExtension) - closedParenthesesIndex - 1] + "(" + str(sameNameCounter) + ")" + "." + fileExtension
                except :
                    tempItem = tempItem[:len(tempItem) - len(fileExtension) - 1] + "(2)." + fileExtension
            else :
                tempItem = tempItem[:len(tempItem) - len(fileExtension) - 1] + "(2)." + fileExtension

        else :
            for i in range(len(tempItem) - 1, 0, -1) :
                if (openParentheses and tempItem[i] != "(" and not closedParentheses) :
                    sameNameCounter += tempItem[i]
                    closedParenthesesIndex += 1
                if (tempItem[i] == ")") :
                    openParentheses = True
                if (tempItem[i] == "(" and openParentheses) :
                    closedParentheses = True
            sameNameCounter = sameNameCounter[::-1]

            if (openParentheses and closedParentheses) :
                try :
                    sameNameCounter = int(sameNameCounter) + 1
                    tempItem = tempItem[:len(tempItem) - closedParenthesesIndex] + "(" + str(sameNameCounter) + ")"
                except :
                    tempItem = tempItem + "(2)"
            else :
                tempItem = tempItem + "(2)"

    return tempItem

# Append all files extensions into ListOfPaths list and also creates the specific folders into the given path
def TheOrganizer(inputPath) :
    global ListOfExtensions, ListOfPaths, counter, newFoldersNames
    noExtension = "No Extensions Files"
    tempItem = ""

    for item in os.listdir(inputPath) :
        if (not os.path.isdir(inputPath + item)) :
            if ("." in item) :
                fileExtension = FindFileExtension(item)
                if (fileExtension not in ListOfExtensions) :
                    ListOfExtensions.append(fileExtension)
                    folderName = fileExtension.upper() + " Files"
                    newOutputPath = outputPath + folderName
                    ListOfPaths.append(newOutputPath)
                    newFoldersNames.append(folderName)
                    if (folderName not in os.listdir(outputPath)) :
                        os.mkdir(newOutputPath)
            else :
                if (noExtension not in ListOfExtensions) :
                    newOutputPath = outputPath + noExtension
                    ListOfPaths.append(newOutputPath)
                    newFoldersNames.append(noExtension)
                    if (noExtension not in os.listdir(outputPath)) :
                        os.mkdir(newOutputPath)

        else:
            if (item not in newFoldersNames) :
                TheOrganizer(inputPath + item + "/" )

    lenOfPaths = len(ListOfPaths)

    # For each file in path we check, if file Extension == with the i file name, so we can move the correct files into the correct folder
    for item in os.listdir(inputPath) :
        finalInputPath = ""
        finalOutputFile = ""
        if (not os.path.isdir(inputPath + item)) :
            if ("." in item) :
                fileExtension = FindFileExtension(item)
                for i in range(lenOfPaths) :
                    pathNameExt = (FindFolderExtension(ListOfPaths[i]).lower() if fileExtension.islower() else FindFolderExtension(ListOfPaths[i]).upper())      # We do this if to take the right Extension (upper or lower)
                    if (fileExtension == pathNameExt) :
                        finalInputPath = inputPath + item
                        tempItem = checkSameFiles(item, ListOfPaths[i])
                        finalOutputFile = ListOfPaths[i] + "/" + tempItem
                        
            else :
                tempItem = checkSameFiles(item, outputPath + noExtension)
                finalInputPath = inputPath + item
                finalOutputFile = outputPath + noExtension + "/" + tempItem

            os.rename(finalInputPath, finalOutputFile)
            counter += 1
        else:
            if (item not in newFoldersNames) :
                TheOrganizer(inputPath + item + "/")


TheOrganizer(inputPath)
DeleteEmptyFolders(inputPath)
#CreateFordersByDate(inputPath) #Even beter sorting

print("\n\nOrganizer, successfully organized", counter, "files.")
print("This window will close in about 5 sec. Thanks for the use. \nHave a good day, or night!")
time.sleep(8)