#!/usr/bin/env python3
#-*- coding:Utf-8 -*-

# ********** What ? **********
#
# De quoi effacer tes messages dans Mattermost

# ********** How ? **********
#
# PEP8 inspired : 
#   https://www.python.org/dev/peps/pep-0008/
# Licence GNU GPL v3.0 :
#   https://www.gnu.org/licenses/gpl.html
# Mattermost API Doc : 
#   https://api.mattermost.com/
# Mattermost driver source : 
#   https://vaelor.github.io/python-mattermost-driver

# ********** Who's to blame ? **********
#
# Credit blablapookie@tartiflet.com

# ********** What now ? **********
#
# 

#####################################################################72

from mattermostdriver import Driver

# un bete fichier.py avec my_login="toto" et my_password="tata"
from MyServerConfig import myServer, myLogin, myPassword

# taille de la pagination des messages, par défaut c'est 60
PER_PAGE = 200 

foo = Driver({
    'url': myServer,
    'login_id': myLogin,
    'password': myPassword,
    'scheme': 'https',
    'port': 443,
    'basepath': '/api/v4',
    'verify': True,
    'timeout': 30,
    'request_timeout': None,
    'debug': False
    })

# on parcoure un set de messages et on les supprime s'ils sont à nous 
# ici ce qui est degueu (entre autre) c'est que la ref à myUserID 
# est déclarée en dehors de la fonction
def delete_posts(handler,msg_list):
   for msg_id in msg_list: 
      msg=foo.posts.get_post(msg_id)
      if(msg['user_id'] == myUserID):
#         print(msg['message'])
         print("Pouet ==> Pan ==> -=RIP=-")

         foo.posts.delete_post(msg_id)

foo.login()
myuser = foo.users.get_user_by_username(myLogin)
myUserID = myuser['id']
myTeam = foo.teams.get_user_teams(myUserID)
myTeamID = myTeam[0]['id']
myChannelsList = foo.channels.get_channels_for_user(myUserID, myTeamID)
for myChannel in myChannelsList: #parcours de mes chans
   myChannelID = myChannel['id']
   page = 0
   myChannelMessageLength = 1
# tant qu'il reste des messages dans le set de msg de la page
   while(myChannelMessageLength != 0): 
# provient de l'API V4, et permet d'accéder 
# à des options supplémentaires
      options={ 
         'page': page,
         'per_page': PER_PAGE
         }

      myChannelsMessageList = foo.posts.get_posts_for_channel(
         myChannelID, 
         options
         )
      myChannelMessage = myChannelsMessageList['order']
      myChannelMessageLength = len(myChannelMessage)
      print(
         "taille :"
         + str(myChannelMessageLength)
         + " - page :"
         + str(page)
         )
# si on est dans un set de msg avec une seule page
      if(myChannelMessageLength < PER_PAGE): 
         delete_posts(foo, myChannelMessage)
         break
# s'il y a plusieurs pages, on boucle
      else: 
         delete_posts(foo, myChannelMessage)
         page = page+1

foo.logout()