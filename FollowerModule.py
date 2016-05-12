import random
import tweepy
from tweepy import TweepError


class FollowerModule():

    def __init__(self, keys):
        self.consumer_key = keys['consumer_key']
        self.consumer_secret = keys['consumer_secret']
        self.access_token = keys['access_token']
        self.access_token_secret = keys['access_token_secret']
        self.api = None
        self.auth()

    def auth(self):
        auth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)

        auth.set_access_token(self.access_token,self.access_token_secret)
        self.api = tweepy.API(auth)

    def followRandomPeopleOnTopic(self, topic, num_followers=5):
        #search topic for tweets, should work on hashtags too

        #filter to english only, defaults to 15 results
        # use count= to get more max = 100
        try:
            results = self.api.search(topic, lang='en', count=100)
        except TweepError, e:
            #handle errors here, e.g rate limit exceeded
            return

        #pick 5 tweets and follow their users
        selectedresults = random.sample(results, num_followers)

        for result in selectedresults:
            #Only try to follow if we are not already following the person / have sent a request already
            self.followUserWithChecks(result.user);
        return

    def followRandomFollowersOfYourOwnFollowers(self, num_own_followers= 5, follower_per_follower =5):
        self.followRandomFollowersOfYourOwnFollowersBase(num_own_followers, follower_per_follower, False)

    def followRandomFollowersOfYourOwnFollowersWithSentiment(self, num_own_followers= 5, follower_per_follower =5):
        self.followRandomFollowersOfYourOwnFollowersBase(num_own_followers, follower_per_follower, True)


    def followRandomFollowersOfYourOwnFollowersBase(self, num_own_followers= 5, follower_per_follower =5, sentiment=True):
        #get list of my own followers
        myFollowerList = self.getListOfUserFollowing(); #no param points to authenticated user

        if len(myFollowerList) < num_own_followers:
            num_own_followers = len(myFollowerList)

        myRandomFollowerList = random.sample(myFollowerList, num_own_followers)

        for user in myRandomFollowerList:
            userFollowerList= self.getListOfUserFollowing(user.screen_name)

            if len(myFollowerList) < follower_per_follower:
                follower_per_follower = len(userFollowerList)

            userRandomFollowerList = random.sample(userFollowerList, follower_per_follower)

            for newUser in userRandomFollowerList:
                if sentiment:
                    sentimentOk = self.checkUserSentiment(newUser)
                    if sentimentOk:
                        self.followUserWithChecks(newUser)

                else:
                    self.followUserWithChecks(newUser)

    def checkUserSentiment(self, user):
        #get latest tweets of user, default 20
        tweetList = []
        try:
            tweetList = self.api.user_timeline(screen_name= user.screen_name, count=20)

            #run sentiment analysis here
            print "SENTIMENT ANALYSIS"
            return True

        except TweepError, e:
            return False


    #returns list of ids
    def getListOfUserIdsFollowed(self,user_id):

        idList = []
        try:
            idList = self.api.friends_ids(user_id=user_id)
        except TweepError, e:
            #handle errors here, e.g rate limit exceeded
            return[]
        return idList

    #return list of users
    def getListOfUserFollowing(self,screen_name=None):

        userList = []
        try:
            #return list of people following screen_name, default 100 users
            userList = self.api.followers(screen_name=screen_name)
        except TweepError, e:
            #handle errors here, e.g rate limit exceeded
            return []
        return userList

    def followUserViaScreenName(self, screen_name):
        try:
            #self.api.create_friendship(screen_name=screen_name)
            return
        except TweepError, e:
            print e.args

    def followUserWithChecks(self, user):
        if (not (user.follow_request_sent or user.following)):
                print user
                print "Following " + str(user.screen_name)
                self.followUserViaScreenName(user.screen_name)


if __name__ == '__main__':
    #quick debugging
    keys = {}
    keys['consumer_key'] = ''
    keys['consumer_secret'] = ''
    keys['access_token'] = ""
    keys['access_token_secret'] = ""
    follow = FollowerModule(keys)
    #follow.followRandomPeopleOnTopic("#Beatles", 5)
    #follow.followRandomFollowersOfYourOwnFollowers()
    #follow.followRandomFollowersOfYourOwnFollowersWithSentiment()