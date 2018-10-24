# GitReposAndStars
Returns a certain number of repositories and stargazers (3 levels deep) for a given name.

GitReposAndStars is an api endpoint designed to grab the repositories of a given userId (up to 3), and then the stargazers of those repos (up to 3 per repo). It takes those gazers and finds their repos (again, up to three followers). It takes those repos and finds their gazers (again, up to 3 gazers per repo).

This repo is a derivation of the GitFollowers code and has been refined slightly (introduction of a class constructor, better abstraction).

For api implementation:

Make sure you have both git and python (3.7) installed locally, or that you are able to run both on your PC. Make sure you've downloaded and installed Flask as well(http://flask.pocoo.org/docs/1.0/installation/) .

You may want to register this as an app to obtain a client ID and secret from github during testing.

Download the code in this repo locally. Make sure that all files have downloaded successfully. The api (main) folder should have 3 files (current as of 10/24/2018).

Start the api by running the api script on the command line (after navigating to the folder with the api from the command line, use "python api.py", without quotes. This may be slightly different depending on your python version and OS. This was done in Windows 10 in the terminal.) Navigation tips: can do "cd" to change the directory (no quotes), and if you use quote marks around the file path, you don't have to use escape characters on spaces in the file name. Ex: cd "C:\Downloads\VMTest\GitFollowers\api" , and then you can start the program.

Navigate the api by going to the appropriate page:

Homepage: http://127.0.0.1:5000/

ReposAndGazers page: http://127.0.0.1:5000/api/v1/resources/followers?id=NAME&maxNumGazers=NUMBER&maxNumRepos=NUMBER ,
replacing NAME with the username of the GitHub user searched for, and NUMBER with the max number of stargazers or repos per user you want returned (maximum is no more than 3 per user). 

Full example URL: http://127.0.0.1:5000/api/v1/resources/reposandgazers?id=palantir&maxNumGazers=2&maxNumRepos=1

Note that:

maxNumRepos and maxNumGazers are an OPTIONAL parameter. The program has a default of 3 for each. It can be omitted from the query without issue.
Both will be capped at 3 to prevent timeouts on the PC (each call will increase the base by a power of 3 for EACH. It will get large quickly).
Finally, this is currently an unauthenticated application. As such, there can only be so many requests from the same IP per hour before the user is prevented from using the website. You may need to set up a client ID and secret and enter them on your computer in order to properly test this program.

From https://developer.github.com/v3/#rate-limiting:

"For unauthenticated requests, the rate limit allows for up to 60 requests per hour. Unauthenticated requests are associated with the originating IP address, and not the user making requests."

Testing and ways to test (if server is running from api.py script, clicking these links will produce the result described):

The easiest way to test this project is to just enter some data in the address bar. For example:

A user that doesn't exist: http://127.0.0.1:5000/api/v1/resources/reposandgazers?id=animeInaction

Produces error page.
Should produce the error message page.


A user that will have a very small (less than 5) result tree: http://127.0.0.1:5000/api/v1/resources/reposandgazers?id=AshleyBushCoding


A user that will have no result tree: http://127.0.0.1:5000/api/v1/resources/reposandgazers?id=DuilioAquino


No user name: 
http://127.0.0.1:5000/api/v1/resources/reposandgazers
Produces error page.
Shows code handles that exception appropriately

No user name but max stargazers: http://127.0.0.1:5000/api/v1/resources/reposandgazers?maxNumGazers=3
Produces error page.
Shows code will properly deal with missing entries


A user name with improper symbols: http://127.0.0.1:5000/api/v1/resources/reposandgazers?id=j^skeet
Produces error page.
Shows code will properly deal with missing entries.

A user that will return a mostly full list:
http://127.0.0.1:5000/api/v1/resources/reposandgazers?id=Palantir&maxNumGazers=3
Shows code can produce a larger list (proof of concept)

Repeated calls to trigger the IP block: 
http://127.0.0.1:5000/api/v1/resources/reposandgazers?id=Palantir&maxNumGazers=3&maxNumRepos=3

Do this two or three times.

Will display error message.


NOTE tester will be prevented from testing at this point for ~ 1 hr!!!
