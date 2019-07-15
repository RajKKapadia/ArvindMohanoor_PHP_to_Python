# ArvindMohanoor_PHP_to_Python
This is a freelance repository for Arvind Mohanoor, and I am converting an existing PHP code to Python.

## Pre-requisite :point_right: Python 3.7.3, SQlite, NGROK
- install pipenv
- copy the repository to folder
- cd into folder
- run `pipenv --python 3.7` then `pipenv sync`

## NGROK part
- run `ngrok http 5000` in new terminal or if you have downloaded the execuitabel from [NGROK](https://ngrok.com/download)
then you can run `./ngrok http 5000`

It will start a link between your local machine and internet, you copy any of the **forwarding link** as shown in below image.

NGROK terminal view

![NGROK Image](/images/ngrok.png)

## Flask part
- run `pipenv run python processWebhook.py`

this will start a local server, make sure flask server port and ngrok server port is same, if not then stop ngrok and restart
with the port you got from local server by running above code.

## Dialogflow Part
- create new bot
- from bot settings :point_right: Export/Import :point_right: Import from zip upload the BirthDateBot.zip or FilghtBooking.zip
- on main dashboard of agent go to Fullfilments
- Enable webhook
- copy the forwarding link from ngrk terminal and paste there and append /webhook
ngrk-link/webhook

Now you are ready to test the bot.

## RESTDB.IO
May be your restdb.io database for Planets tutorial differ from The one I have used, so for reference see the databse structure
for Planets.

Restdb.io Planets Databse Image

![RESTDB.IO Image](/images/restdb.io.png)
