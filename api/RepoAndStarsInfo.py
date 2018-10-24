class ReposAndStarsInfo:
    
    def __init__(self, initialUserId, maxGazers = 3, maxRepos= 3):
        self.initialId = initialUserId
        self.maxNumRepos = maxRepos
        self.maxNumGazers = maxGazers
        self.gazerList = []
        self.repoList = []
        self.finalList = []
        self.errMessage = []
        self.errorThrown = False