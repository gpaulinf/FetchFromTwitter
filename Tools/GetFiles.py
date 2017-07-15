'''
    Author: Fernando Paulin
    Version: 1.0
    Developed: July the 14th, 2017.
    This class provides different Tools for File Management
'''


'''IMPORTS'''
import urllib, random, os.path, pickle, pandas as pd



class GetFile():

    def __init__(self):
        ''' Constructor'''
        pass

    def __del__ (self):
        '''Destructor'''
        pass

    def GetFileFromURL(self,url,fileName,hashtag):
        '''Downloads file from a URL. It is intended to be download only Images, but it can be used for any file'''
        self.makeFolder(hashtag, "Images")
        RouteToFile = self.FolderName+"/"+fileName
        if (self.ShouldDownload(RouteToFile, url)):
            urllib.request.urlretrieve(url,RouteToFile)

    def makeFolder(self,hashtagOrUsername, type):
        '''Makes a Folder with the specified Foldername if it doesn't exist'''
        if hashtagOrUsername[0]=="#": self.FolderName = type+'_'+hashtagOrUsername[1:]
        else: self.FolderName=type+'_'+hashtagOrUsername
        if (not os.path.exists(self.FolderName)):
            os.mkdir(self.FolderName)
        else: pass

    def CheckFileExists(self, PathToFile):
        '''Check if a File exists given the name'''
        if not(os.path.exists(PathToFile)):
            return False
        else: return True


    def ShouldDownload(self, filename, url):
        '''Decide if a file should be downloaded given the byte size'''
        try : LocalFileSize =  os.path.getsize(filename)
        except FileNotFoundError: LocalFileSize=0
        CloudFileSize = urllib.request.urlopen(url).info()['Content-Length']
        if (LocalFileSize==CloudFileSize):return False
        else: return True


    def SaveTextToFile(self, HashTagOrUser, text):
        '''Saves text from files to a .txt file'''
        self.makeFolder(HashTagOrUser, "Text")
        RouteToFile = self.FolderName + "/" + HashTagOrUser+".txt"
        with open(RouteToFile, "a") as OpenFile:
            OpenFile.write(text)

    def LoadText(self,HashTagOrUser):
        RouteToFile = "./Text_"+HashTagOrUser+"/"+HashTagOrUser+".txt"
        with open(RouteToFile, "rb") as OpenFile:
            return OpenFile.read()

    def LoadResults(self, HashTagOrUser):
        RouteToFile = "./Text_" + HashTagOrUser + "/" + HashTagOrUser +"_TA"+ ".pckl"
        with open(RouteToFile, 'rb') as File:
            return pickle.load(File)

    def SaveTAResults(self, Text, HashTagOrUser):
        RouteToFile = "./Text_" + HashTagOrUser + "/" + HashTagOrUser +"_TA"+ ".pckl"
        with open(RouteToFile, 'wb') as File:
            return pickle.dump(Text, File)

    def GenerateRouteToFile(self, HashtagOrUser,Type, Extension):
        return (Type+'_'+HashtagOrUser+'/'+HashtagOrUser+Extension)


    def PrepareData(self, Data, HashTagOrUser):
        RouteToFile = "./Text_" + HashTagOrUser + "/" + HashTagOrUser + "_DB" + ".xlsx"
        if (not self.CheckFileExists(RouteToFile)):
            df = pd.DataFrame(columns =('TEXT', 'Anger', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Analytical', 'Confident', 'Tentative', 'Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Emotional Range'))
        else: df = pd.DataFrame()
        GeneralResults = ["GENERAL SCORE: "]
        DocumentResults = Data[:Data.find('sentences_tone')]
        for line in DocumentResults.split("},{"):
            Split = (line[line.index("score"):].split(":"))
            Score = Split[1].split(",")[0]
            GeneralResults.append(float(Score))
        DocumentResults = Data[Data.find('sentences_tone'):]
        Split = DocumentResults.split('"sentence_id"')
        df.loc[0] = GeneralResults
        Categories = ['TEXT']
        for i,line in enumerate(Split):
            try:
                Text = line[line.index('"text":'):line.index(',"input_from"')].split(":")[1]
                ToneCategories = line[line.index('"tone_categories":[{"tones":') + len(
                    '"tone_categories":[{"tones":'):line.index(',"category_id"')]
                ToneScores = ToneCategories.split('{"score":')
                EmotionTone = line[line.index('"Emotion Tone"},{"tones":') + len('"Emotion Tone"},{"tones":'):]
                EmotionScores = EmotionTone.split('{"score":')
                scores = []
                for value in ToneScores:
                    if ("tone_id" in value):
                        score = value.split(",")[0]
                        scores.append(float(score))
                        if (len(Categories) < 6):
                            Category = value[value.index('"tone_name":"') + len('"tone_name":"'):value.index('"}')]
                            Categories.append(Category)
                for value in EmotionScores:
                    if ("tone_id" in value):
                        score = value.split(",")[0]
                        scores.append(float(score))
                        if (len(Categories) < 14):
                            Category = value[value.index('"tone_name":"') + len('"tone_name":"'):value.index('"}')]
                            Categories.append(Category)
                df.loc[i]=[Text]+scores
            except ValueError:
                pass
        writer = pd.ExcelWriter(RouteToFile, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
