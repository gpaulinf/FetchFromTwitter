from Tools.TweetTools import TweetTools
from Tools.GetFiles import GetFile
from Tools.ToneAnalyser import ToneAnalyser
from sys import getsizeof
from pickle import dump, load

TT = TweetTools()
TA = ToneAnalyser()
GF = GetFile()

HashTagOrUser = "realDonaldTrump"

'''TWITTER CREDENTIALS'''
TT.AuthenticateInTwitter()

'''FUNCTIONS'''
#TT.PostInTwitter("")
#TT.RetrieveImagesFromHashtag([""],[1000])
#TT.FetchImagesFromUser([''],[2500])


'''
TT.RetrieveTextFromUser(["realDonaldTrump"],[600])


Text = GF.LoadText(HashTagOrUser)

if not(GF.CheckFileExists(GF.GenerateRouteToFile(HashTagOrUser, 'Text',"_TA"+ ".pckl"))):
    GF.SaveTAResults(TA.AnalyseTone(Text), HashTagOrUser)
Results = GF.LoadResults("realDonaldTrump")
GF.PrepareData(Results, "realDonaldTrump")

'''












'''
ToFind = 'sentences_tone'
GeneralResults = ["GENERAL SCORE: "]
ParticularResults = []
DocumentResults = Results[:Results.find(ToFind)]
for line in DocumentResults.split("},{"):
    Split = (line[line.index("score"):].split(":"))
    Score =  Split[1].split(",")[0]
    GeneralResults.append(float(Score))
DocumentResults = Results[Results.find(ToFind):]
Test = DocumentResults.split('"sentence_id"')
ParticularScores = []
Categories=['TEXT']
for line in Test:
    try:
        Text = line[line.index('"text":'):line.index(',"input_from"')].split(":")[1]
        ToneCategories = line[line.index('"tone_categories":[{"tones":')+len('"tone_categories":[{"tones":'):line.index(',"category_id"')]
        ToneScores = ToneCategories.split('{"score":')
        EmotionTone = line[line.index('"Emotion Tone"},{"tones":')+len('"Emotion Tone"},{"tones":'):]
        EmotionScores = EmotionTone.split('{"score":')
        scores = []
        for value in ToneScores:
            if ("tone_id" in value):
                score = value.split(",")[0]
                scores.append(float(score))
                if (len(Categories)<6):
                    Category = value[value.index('"tone_name":"')+len('"tone_name":"'):value.index('"}')]
                    Categories.append(Category)
        for value in EmotionScores:
            if ("tone_id" in value):
                score = value.split(",")[0]
                scores.append(float(score))
                if (len(Categories)<14):
                    Category = value[value.index('"tone_name":"')+len('"tone_name":"'):value.index('"}')]
                    Categories.append(Category)
        print ([Text]+scores)
    except ValueError: pass

    print (100*"-")
    print ("\n")

print (Categories)
print (GeneralResults)

while index < len(Results):
    index = Results.find(ToFind, index)
    if index == -1:
        break
    print('Found at', index)
    index += len(ToFind)
'''
