'''
    Author: Fernando Paulin
    Version: 1.0
    Developed: July the 14th, 2017.
    Different tools provided for tweet Management
'''


'''IMPORTS'''
import pickle, os.path, tweepy
from Tools.GetFiles import GetFile



class TweetTools():

    def __init__(self):
        self.GF = GetFile()

    def __del__(self):
        self.KeysDirectory.clear()

    def LoadAuthData(self,name='AuthData.pckl'):
        if (not os.path.exists(name)):
            self.KeysDirectory = self.GenerateNewKeysFile()
        else:
            with open (name, 'rb') as File:
                self.KeysDirectory = pickle.load(File)
        return self.KeysDirectory

    def GenerateNewKeysFile(self):
        print ("KEY FILE NOT FOUND. PLEASE PROVIDE THE FOLLOWING INFORMATION \n")
        CONSUMER_KEY = input("ADD CONSUMER KEY (API KEY): ")
        CONSUMER_SECRET = input("ADD CONSUMER SECRET (API SECRET): ")
        ACCESS_TOKEN = input("ADD ACCESS TOKEN: ")
        ACCESS_TOKEN_SECRET = input("ADD ACCESS TOKEN SECRET: ")
        KeysDirectory = {'ConsumerKey':CONSUMER_KEY, 'ConsumerSecret':CONSUMER_SECRET, 'AccessToken':ACCESS_TOKEN, 'AccessTokenSecret':ACCESS_TOKEN_SECRET}
        with open('AuthData.pckl', 'wb') as f:
            pickle.dump(KeysDirectory, f)
        return KeysDirectory

    def ValidateInformation(self, information, parameter):
        Answer = input("IS THIS INFORMATION CORRECT FOR {0}: {1}\nANSWER Y/N: ".format(parameter, information))
        if (Answer=='Y' or Answer=='y'): return False
        else: return True

    def AuthenticateInTwitter(self):
        __=self.LoadAuthData()
        auth = tweepy.OAuthHandler(self.KeysDirectory['ConsumerKey'], self.KeysDirectory['ConsumerSecret'])
        auth.set_access_token(self.KeysDirectory['AccessToken'], self.KeysDirectory['AccessTokenSecret'])
        self.api = tweepy.API(auth)

    def PostInTwitter(self, message):
        try:
            self.api.update_status(status=message)
            print ("STATUS:\n{0}\nSUCCESSFULLY POSTED!".format(message))
        except Exception:
            print ("A PROBLEM OCCURRED!: THE MESSAGE: \n {0} \n WAS NOT POSTED".format(message))



    def RetrieveImagesFromHashtag(self, hashtags, HowManyTweetsPerHashtag):
        for i, (hashtag, NumberOfTweets) in enumerate(zip(hashtags,HowManyTweetsPerHashtag)):
            count = 0
            try:
                search = self.api.search(q=hashtag, count=200)
                last_id = search[-1].id
            except IndexError:
                print ("NO TWEETS FOUND")
                break
            while (count < NumberOfTweets):
                try:
                    for tweet in search:
                        try:
                            URL = tweet.extended_entities['media'][0]['media_url_https']
                            self.GF.GetFileFromURL(URL, URL.split("/")[-1], hashtag)
                        except AttributeError:
                            pass
                    count+=len(search)
                    search = self.api.search(q=hashtag, count=200, max_id=last_id - 1)
                    last_id = search[-1].id - 1
                except IndexError:
                    print ("LESS THAN {0} TWEETS WITH THE HASHTAG {1} FOUND".format(count, hashtag))
                    break
            print ("ALL IMAGES FROM HASTHAG: {0} . SUCCESFULLY RETRIEVED".format(hashtag))


    def FetchImagesFromUser(self, users, HowManyTweets):
        for user, NumberOfTweets in zip(users,HowManyTweets):
            count = 0
            try:
                search = self.api.user_timeline(screen_name=user,count=200, include_rts=False,exclude_replies=True)
                last_id = search[-1].id
            except IndexError:
                print ("NO TWEETS FOUND")
                break
            while (count < NumberOfTweets):
                try:
                    for tweet in search:
                        try:
                            URL = tweet.extended_entities['media'][0]['media_url_https']
                            self.GF.GetFileFromURL(URL, URL.split("/")[-1], user)
                        except AttributeError:
                            pass
                    count+=len(search)
                    search = self.api.user_timeline(screen_name=user, count=200, include_rts=False, exclude_replies=True,max_id=last_id - 1)
                    last_id = search[-1].id - 1
                except IndexError:
                    print ("LESS THAN {0} TWEETS FROM THE USER: {1} FOUND".format(count, user))
                    break
            print ("ALL IMAGES FROM USER: {0} . SUCCESFULLY RETRIEVED".format(user))


    def GetSingleTweet(self, user):
        search = self.api.user_timeline(screen_name=user, count=1, include_rts=False, exclude_replies=True)
        return search


    def RetrieveTextFromUser(self, users,HowManyTweets):
        for user, NumberOfTweets in zip(users,HowManyTweets):
            count = 0
            try:
                Tweets = int(0.9* (NumberOfTweets - count))
                search = self.api.user_timeline(screen_name=user,count=Tweets, include_rts=False,exclude_replies=True)
                last_id = search[-1].id
                while (count<=NumberOfTweets):
                    count += len(search)
                    for tweet in search:
                        self.GF.SaveTextToFile(user,tweet.text)
                        #print("TWEET {0}: {1}".format(i+count, tweet.text))
                    Tweets = abs(int(0.6*(NumberOfTweets-count))) if (NumberOfTweets-count>=0) else 1
                    search = self.api.user_timeline(screen_name=user, count=Tweets, include_rts=False, exclude_replies=True,max_id=last_id - 1)
                    last_id = search[-1].id - 1
            except IndexError:
                print ("NO TWEETS FOUND")
                break
