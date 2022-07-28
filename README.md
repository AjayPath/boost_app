# Guide to the Boost App

By: Ajay Path
Date: July 2022

This app was created for demo purposes. It was shown to Salesforce as a MVP and will grow with the help of other developers. The main concept of this app was for companies improve company involvment while also helping them offset their Scope 2 emissions. Users will be able to boost others using boost tokens, represented by the zap emoji within Slack. You will also be able to redeem these boost tokens and power various sites your company have purchused D-RECs from. Yes, the boost tokens are used to symbolize D-REC contracts.

The model of the app will continue to change as we continue to dicuss with Salesforce, but as of this current time this is the methodology behind the app.


## Using the app on Slack
To utilize the app on a slack channel you can use the commands below.

/connect -> add yourself to the database

/total -> view your current total of boost tokens

/distribute -> this will take your current number of boost tokens and share them evenly among users if you have enough
               note: this command has rarely been tested so please avoid using it
               
/reddem -> redeem the boost token to one of the sites in the database

/profile -> bring up a website where you can view your profile

zap emoji -> by zapping someone in a channel where the bot has been added, you can give them a boost token


## Setting up the App
From a coding prespective, to set up the app you will need to dowload all these files into a folder. By running the setup_db.py file you will create a database to hold your values Then create a .env file to hold your slack tokens. You can also create a virtual env and pip install the libraries below:

slack-bolt, folium, flask, python-dotenv


You will also need to create a new app on slack which will be added to your workspace. The specs of the app can be noted below:

Socket Mode -> ON:

interactivity & shorcuts, slack commands, event subscriptions


OAth:

channels:history, chat:write, chat:write.public, commands, groups:history, im:history, mpim:history, reactions:read


Event Subscription -> ON:

message.channel, message.groups, message.im, message.mpim, reaction_added


Slash-Comamnds:

connect, total, distribute, redeem, profile

## How to run the app:
To run the app you will need two different command prompts open. In one prompt the file-path will be the boost_app.py file and the other will have the path for website.py.

CMD:

cd boost_app

cd venv

scripts\activate

python "file-path"
