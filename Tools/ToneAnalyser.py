from pickle import dump, load
import os, requests, json

class ToneAnalyser():

    def __init__(self):
        pass

    def AnalyseTone(self, text):
        __ = self.LoadAuthData()
        headers = {"content-type": "text/plain"}
        #Valid values are application/json, text/html, and plain/text. For example, "Content-Type: text/html"
        try:
            r = requests.post(self.KeysDirectory['url'], auth=(self.KeysDirectory['username'], self.KeysDirectory['password']), headers=headers, data=text)
            return r.text
        except:
            return False


    def LoadAuthData(self,name='ToneAnalyserAuthData.pckl'):
        if (not os.path.exists(name)):
            self.KeysDirectory = self.CreateCredentials()
        else:
            with open (name, 'rb') as File:
                self.KeysDirectory = load(File)
        return self.KeysDirectory


    def CreateCredentials(self):
        print("KEY FILE FOR TONE ANALYSER NOT FOUND. PLEASE PROVIDE THE FOLLOWING INFORMATION \n")
        URL = input("ADD URL: ")
        URL = URL.strip()
        USERNAME = input("ADD USERNAME: ")
        PASSWORD = input("ADD PASSWORD: ")
        KeysDirectory = {'url': URL, 'username': USERNAME,'password': PASSWORD}
        with open('ToneAnalyserAuthData.pckl', 'wb') as f:
            dump(KeysDirectory, f)
        return KeysDirectory