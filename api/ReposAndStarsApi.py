#Requirements: 
# API endpoint that accepts a GitHub ID and retrieves the Repository names (up
# to 3 repositories total) associated with the passed in GitHub ID, along with the
# StarGazer GitHub Id's (up to 3 total) associated with each repo. Do this for 3 levels.
# Return data in JSON format.

#done by Ashley Bush under MIT liscense--have fun!

# NOTE: THE NUMBER OF CALLS TO GITHUB IN THIS PROGRAM WILL ALMOST CERTAINLY REQUIRE
# A TESTER TO REGISTER AN APP FOR A CLIENT ID AND SECRET TO USE. WITHOUT THOSE, THE user
# CAN ONLY DO 60 CALLS TO GITHUB IN AN HOUR. WITH IT, THEY CAN DO ~5000. APPROPRIATE SECTIONS 
# OF THE CODE HAVE BEEN LABELED. SEARCH FOR "client_id" or "client_secret"

import requests #for the API calls
import sys #for errors
from RepoAndStarsInfo import *


def get_gazers(githubOwnerId, repository, maxNumGazers = 3):
    
    # GitHub API extension: /repos/:owner/:repo/stargazers

    #per github v3 API, per_page allows for making a limit on 
    # returned items (up to 100). Without it, returns every follower 
    githubApiLink = "https://api.github.com/repos/" + githubOwnerId + "/" \
     + repository + "/stargazers" + "?per_page=" + str(maxNumGazers) #+ "&client_id=YOURIDHERE&client_secret=YOURSECRETHERE"

    response = requests.get(githubApiLink)
    #Note: JSON response returned may be an error. Valid, but less useful.
    return response.json()


def get_repos(githubId, maxNumRepos = 3):

    #GET /user/repos    
    #per github v3 API, per_page allows for making a limit on 
    # returned items (up to 100). Without it, returns every follower 
    githubApiLink = "https://api.github.com/users/" + githubId + "/repos" \
        + "?per_page=" + str(maxNumRepos) #+ "&client_id=YOURIDHERE&client_secret=YOURSECRETHERE"

    response = requests.get(githubApiLink)
    #Note: JSON response returned may be an error. Valid, but less useful.
    return response.json()

def get_owner(currentRepoDict):
    try:
        innerDictionary = currentRepoDict.get("owner")
        if(innerDictionary is not None):
            return innerDictionary.get("login")
        else:
            return None
    except:
        return 

def get_repo_name(currentRepoDict):
    try:
        return currentRepoDict['name']
    except:
        return 

def get_login(currentRepoDict):
    try:
        return currentRepoDict['login']
    except:
        return 


def getStargazerLevel(repoList, gazerList, maxNumGazers, queryIndex, stopIndex):
    for dictionary in repoList[queryIndex : stopIndex]:
        if(type(dictionary) is dict):
            userId = get_owner(dictionary)
            repoName = get_repo_name(dictionary)
            if(userId is not None and repoName is not None):
                tempGazers = get_gazers(userId, repoName, maxNumGazers)
                #if the list is empty, continue loop. Else, add item.
                if not tempGazers:
                    continue
                gazerList.extend(tempGazers)
        else: #not dictionary, may be error
            try:
                #raise whatever exception occurred
                raise # pylint: disable=E0704 
            except:
                raise TypeError('Incorrect type returned')

    return gazerList

def getRepoLevel(repoList, gazerList, maxNumRepos, queryIndex, stopIndex):
    for dictionary in gazerList[queryIndex : stopIndex]:
        if(type(dictionary) is dict):
            userId = get_login(dictionary)
            if(userId is not None):
                tempRepos = get_repos(userId, maxNumRepos)
                #if the list is empty, continue loop. Else, add item.
                if not tempRepos:
                    continue
                repoList.extend(tempRepos)
        else: #not dictionary, may be error
            try:
                #raise whatever exception occurred
                raise # pylint: disable=E0704 
            except:
                raise TypeError('Incorrect type returned')
    return repoList

def returnError():
    return [{"FollowerErrorMessage" : 
        "An unexpected error occurred. The data may or may not be truncated.\n \
         If you see this message repeatedly, it's likely your IP has been blocked \n \
         on the server. See https://developer.github.com/v3/#rate-limiting."}]

def query_user(githubId, maxNumGazers = 3, maxNumRepos = 3):
    # Note: unauthenticated apps can only so may queries per minute and hour 
    # (might be as low as 60 queries per hour). at 3 levels of calls, 
    # 3 each, for 2 types of calls we're at 3^2 * 2, (first level is 3^0), or 18 or so 
    # calls a min.
    # To do more, app will need to be authenticated.

    queryUser = ReposAndStarsInfo(githubId, maxNumGazers, maxNumRepos)

    tempRepo = get_repos(queryUser.initialId, queryUser.maxNumRepos)

    queryIndexR = 0 #search start point for next round of repos
    queryIndexG = 0 #search start point for next round of gazers
    stopIndex = 0 #stop point on the searches 
    

    # make sure list is not empty--empty lists==false.
    if not tempRepo:
        return

    # make sure before adding anything to the final list
    # that it's legit data.
    for dictionary in tempRepo:
        if(type(dictionary) is dict):
            continue
        else: #not dictionary, may be error
            queryUser.finalList.extend(returnError())
            return queryUser.finalList            

    queryUser.repoList.extend(tempRepo) #tempRepo is a list    

    try:
        #need to iterate loop for 2.5 loops. will break after looping through gazers the 3rd time.
        # loop range is from [0,3) . 3 is not included.
        # list use one another in order to grow, so indexing is based on opposite lists
        # index is marked by the end of iterating over the list, so that's when it's changed
        # iteration is done with a range like [a,b) listed above.
        for x in range(0, 3):
            #get level of stargazers
            stopIndex = len(queryUser.repoList)
            queryUser.gazerList = getStargazerLevel(queryUser.repoList, queryUser.gazerList, queryUser.maxNumGazers, queryIndexR, stopIndex)
            queryIndexR = stopIndex

            
            if(x == 2):
                break

            #get level of repos
            stopIndex = len(queryUser.gazerList)
            queryUser.repoList = getRepoLevel(queryUser.repoList, queryUser.gazerList, queryUser.maxNumGazers, queryIndexG, stopIndex)
            queryIndexG = stopIndex

        #combine the lists to return
        queryUser.finalList.extend(queryUser.repoList)
        queryUser.finalList.extend(queryUser.gazerList)
    except:
        #some sort of error
        queryUser.errMessage.extend([returnError])   
        queryUser.errorThrown = True

    return queryUser.finalList

def validAlphaNumOrHyphen(userId):
    for character in userId:
        if(not character.isalnum() and character is not "-"):
            return False
    #else it's good to go
    return True


if __name__ == '__main__':
    print("Please use the api to access this code.\n \
    Please enter userId of the GitHub member you are finding the \n \
    repos and stargazers for at the end of the website. You can also \n \
    optionally add in the number of repos and gazers referenced (up to 3). \n \
    Ex: http://127.0.0.1:5000/api/v1/resources/reprosandgazers?id=jskeet&maxNumGazers=2")

      