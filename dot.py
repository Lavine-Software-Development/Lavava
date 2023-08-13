import pygame as p

import math

import time

p.init()

screen=p.display.set_mode((600,600))

p.display.update()

####colours

WHITE=(255,255,255)

BLACK=(0,0,0)

RED=(255,0,0)

BLUE=(0,0,255)

GREEN=(0,255,0)

YELLOW=(50,250,250)

GREY=(120,120,120)

####images

####hearts 1, clubs 2, diamonds 3, spades 4

heart=p.image.load('heart.jpg')

club=p.image.load('club.jpg')

diamond=p.image.load('diamond.jpg')

spade=p.image.load('spade.jpg')

checkmark=p.image.load('checkmark.jpg')

######screen vars

mode=0

hand=[[1,1],[1,1],[1,1]]

hand2=[[1,1],[1,1],[1,1]]

cardsinhand=0

suitcol=[RED,BLACK,RED,BLACK]

cardvalue=['A','K','Q','J','10','9','8','7','6','5','4','3','2']

######math vars

carddeck=([[14,1],[14,2],[14,3],[14,4],[13,1],[13,2],[13,3],[13,4],[12,1],[12,2],[12,3],[12,4],[11,1],[11,2],[11,3],[11,4],[10,1],[10,2],[10,3],[10,4],[9,1],[9,2],[9,3],[9,4],[8,1],[8,2],[8,3],[8,4],[7,1],[7,2],[7,3],[7,4],[6,1],[6,2],[6,3],[6,4],[5,1],[5,2],[5,3],[5,4],[4,1],[4,2],[4,3],[4,4],[3,1],[3,2],[3,3],[3,4],[2,1],[2,2],[2,3],[2,4]])

win=0

lose=0

tie=0

noplay=0

####font

font = p.font.Font(None, 110)

font2 = p.font.Font(None, 60)

font3 = p.font.Font(None, 40)

font4 = p.font.Font(None, 30)

title = p.font.Font(None, 300)

#####math functions

def remove(carddeck,cards):

    carddeck.remove(cards[0])

    carddeck.remove(cards[1])

    carddeck.remove(cards[2])

   

def handdecide(hand):

    if (hand[0][0]-2)==(hand[1][0]-1)==(hand[2][0]) and hand[0][1]==hand[1][1]==hand[2][1] or hand[0][0]==14 and hand[1][0]==3 and hand[2][0]==2 and hand[0][1]==hand[1][1]==hand[2][1]:

        playerhandlevel=6

    else:

        if hand[0][0]==hand[1][0]==hand[2][0]:

            playerhandlevel=5

        else:

            if (hand[0][0]-2)==(hand[1][0]-1)==(hand[2][0]) or hand[0][0]==14 and hand[1][0]==3 and hand[2][0]==2:

                playerhandlevel=4

            else:

                if hand[0][1]==hand[1][1]==hand[2][1]:

                    playerhandlevel=3

                else:

                    if hand[0][0]==hand[1][0] or hand[1][0]==hand[2][0]:

                        playerhandlevel=2

                    else:

                        playerhandlevel=1

    return(playerhandlevel)

 

def dealercard(cards,hand,playerhandlevel,win,lose,tie,noplay):

    if hand[0][0]<hand[1][0]:

        filler=hand[0]

        hand[0]=hand[1]

        hand[1]=filler

    if hand[1][0]<hand[2][0]:

        filler=hand[1]

        hand[1]=hand[2]

        hand[2]=filler

    if hand[0][0]<hand[1][0]:

        filler=hand[0]

        hand[0]=hand[1]

        hand[1]=filler   

    for x in range(0,(len(cards)-2)):

        for y in range(x+1,len(cards)-1):

            for z in range(y+1,len(cards)):

                if (cards[x][0]-2)==(cards[y][0]-1)==(cards[z][0]) and cards[x][1]==cards[y][1]==cards[z][1] or cards[x][0]==14 and cards[y][0]==3 and cards[z][0]==2 and cards[x][1]==cards[y][1]==cards[z][1]:

                    dealerhandlevel=6

                else:

                    if cards[x][0]==cards[y][0]==cards[z][0]:

                        dealerhandlevel=5

                    else:

                        if (cards[x][0]-2)==(cards[y][0]-1)==(cards[z][0]) or cards[x][0]==14 and cards[y][0]==3 and cards[z][0]==2:

                            dealerhandlevel=4

                        else:

                            if cards[x][1]==cards[y][1]==cards[z][1]:

                                dealerhandlevel=3

                            else:

                                if cards[x][0]==cards[y][0] or cards[y][0]==cards[z][0]:

                                    dealerhandlevel=2

                                else:

                                    dealerhandlevel=1

                if dealerhandlevel==1 and cards[x][0]<12:

                    noplay+=1

                else:

                    if dealerhandlevel>playerhandlevel:

                        lose+=1

                    elif playerhandlevel>dealerhandlevel:

                        win+=1

                    elif playerhandlevel==dealerhandlevel:

                        if dealerhandlevel==1:

                            if cards[x][0]>11:

                                if cards[x][0]>hand[0][0]:

                                    lose+=1

                                elif hand[0][0]>cards[x][0]:

                                    win+=1

                                else:

                                    if cards[y][0]>hand[1][0]:

                                        lose+=1

                                    elif hand[1][0]>cards[y][0]:

                                        win+=1

                                    else:

                                        if cards[z][0]>hand[2][0]:

                                            lose+=1

                                        elif hand[2][0]>cards[z][0]:

                                            win+=1

                                        else:

                                            tie+=1

                        elif playerhandlevel==2:

                            playertie=hand[0][0]

                            playerother=hand[2][0]

                            dealertie=cards[x][0]

                            dealerother=cards[z][0]

                            if playertie!=hand[1][0]:

                                playertie=hand[1][0]

                                playerother=hand[0][0]

                            if dealertie!=cards[y][0]:

                                dealertie=cards[y][0]

                                dealerother=cards[x][0]

                            if dealertie>playertie:

                                lose+=1

                            elif playertie>dealertie:

                                win+=1

                            else:

                                if dealerother>playerother:

                                    lose+=1

                                elif playerother>dealerother:

                                    win+=1

                                else:

                                    tie+=1

                        else:

                            if cards[x][0]>hand[0][0]:

                                lose+=1

                            elif hand[0][0]>cards[x][0]:

                                win+=1

                            else:

                                if cards[y][0]>hand[1][0]:

                                    lose+=1

                                elif hand[1][0]>cards[y][0]:

                                    win+=1

                                else:

                                    if cards[z][0]>hand[2][0]:

                                        lose+=1

                                    elif hand[2][0]>cards[z][0]:

                                        win+=1

                                    else:

                                        tie+=1

    total=win+lose+tie+noplay

    winpct=math.floor((win/total)*1000)/10

    losepct=math.floor((lose/total)*1000)/10

    noplaypct=math.floor((noplay/total)*1000)/10

   

    oddsscreen(winpct,losepct,noplaypct)

 

def poker_remove(carddeck,hands):

    for i in length(hands):

        hand=hands[i]

        carddeck.remove(hand[0])

        carddeck.remove(hand[1])

 

####screen functions

def oddsscreen(winpct,losepct,noplaypct):

    screen.blit(font2.render(str(winpct),True,GREEN),(460,54))

    screen.blit(font2.render(str(losepct),True,RED),(460,162))

    screen.blit(font2.render(str(noplaypct),True,YELLOW),(460,272))

   

    p.display.update()

   

def startmenu():

    screen.fill(BLACK)

    p.draw.rect(screen,RED,(50,70,500,200))

    screen.blit(font.render("3-Card Poker",False,WHITE),(60,130))

    p.draw.rect(screen,GREEN,(50,330,500,200))

    screen.blit(font.render("Blackjack",False,WHITE),(111,390))

    p.display.update()

 

def gamemenu():

    screen.fill(BLACK)

    p.draw.rect(screen,GREY,(30,30,120,50))

    screen.blit(font2.render("Back",False,BLACK),(35,35))

    screen.blit(font3.render("Enter the number of players",False,WHITE),(100,120))

    screen.blit(font3.render("at your table (one or two):",False,WHITE),(100,160))

    p.display.update()

 

def pokermenu(players):

    screen.fill(BLACK)

    p.draw.rect(screen,GREY,(0,450,600,150))

    for x in range(0,4):

        for y in range(0,13):

            p.draw.rect(screen,WHITE,((20+150*x),(11+33*y),110,26))

            if x==0:

                screen.blit(heart,(100,12+33*y))

            elif x==1:

                screen.blit(club,(250,12+33*y))

            elif x==2:

                screen.blit(diamond,(400,12+33*y))

            else:

                screen.blit(spade,(550,12+33*y))

            screen.blit(font4.render(cardvalue[y],False,suitcol[x]),(50+150*x,12+33*y))

    if players==1:

        p.draw.rect(screen,BLACK,(220,475,160,115))

        screen.blit(font4.render("Your Hand",True,WHITE),(244,454))

    elif players==2:

        p.draw.rect(screen,BLACK,(95,475,160,115))

        screen.blit(font4.render("Your Hand",True,WHITE),(119,454))

        p.draw.rect(screen,BLACK,(345,475,160,115))

        screen.blit(font4.render("Friend's Hand",True,WHITE),(355,454))

    p.display.update()

 

def tcp_showodds(win,lose,tie,noplay):

    screen.fill(GREY)

    screen.blit(font2.render("Win percentage: ",True,WHITE),(30,50))

    screen.blit(font2.render("Lose percentage: ",True,WHITE),(30,160))

    screen.blit(font2.render("No Play percentage: ",True,WHITE),(30,270))

    p.draw.rect(screen,RED,(100,400,400,180))

    screen.blit(font.render("Restart",False,WHITE),(154,460))

    p.display.update()

#####################

startmenu()

running=True

 

######

 

######

#mode 0 is start menu where user is choosing the gamemode

#mode 1 is the menu where the user is selecting the number of players

#mode 2 is the screen with all of the cards and the user chooses the hands

#mode 3 is the screen where the odds are displayed

while running:

    for event in p.event.get():

        if event.type == p.QUIT:

            running= False

        elif event.type == p.MOUSEBUTTONDOWN:

            position=event.pos

            if mode==0:

                players=0

                if 50<position[0]<550:

                    if 70<position[1]<270:

                        mode=1

                        gamemenu()

                    elif 330<position[1]<530:

                        print("")

                        print("**************************")

                        print("BlackJack is")

                        print("under development!")

                        print("**************************")

                        print("")

            elif mode==1 or mode==-1:

                if 30<position[0]<150 and 30<position[1]<80:

                    mode=0

                    startmenu()

                elif players==1 or players==2:

                    handsfilled=0

                    pokermenu(players)

                    mode=mode*2

            elif mode==2:

                if cardsinhand<3:

                    if 20<position[0]<130 or 170<position[0]<280 or 320<position[0]<430 or 470<position[0]<580:

                        if 11<position[1]<37 or 44<position[1]<70 or 77<position[1]<103 or 110<position[1]<136 or 143<position[1]<169 or 176<position[1]<202 or 209<position[1]<235 or 242<position[1]<268 or 275<position[1]<301 or 308<position[1]<334 or 341<position[1]<367 or 374<position[1]<400 or 407<position[1]<433:

                             suit=math.floor(position[0]/150)+1

                             number=14-math.floor((position[1]-11)/33)

                             already_clicked=False

                             if handsfilled==0:

                                 for i in range(0,3):

                                     if hand[i]==[number,suit]:

                                         already_clicked=True

                                 if not already_clicked: 

                                     hand[cardsinhand]=[number,suit]

                                     p.draw.rect(screen,WHITE,(105+125*(2-players),485+cardsinhand*35,140,27))

                                     screen.blit(font4.render(cardvalue[14-number],False,suitcol[suit-1]),(125+125*(2-players),490+cardsinhand*35))

                                     p.draw.rect(screen,BLACK,((20+150*(suit-1)),(11+33*(math.floor((position[1]-11)/33))),110,26))

                                     if suit==1:

                                         screen.blit(heart,(205+125*(2-players),486+cardsinhand*35))

                                     elif suit==2:

                                         screen.blit(club,(205+125*(2-players),486+cardsinhand*35))

                                     elif suit==3:

                                         screen.blit(diamond,(205+125*(2-players),486+cardsinhand*35))

                                     else:

                                         screen.blit(spade,(205+125*(2-players),486+cardsinhand*35))

                                     cardsinhand+=1

                             if cardsinhand==3:

                                 handsfilled+=1

                                 if handsfilled==players:

                                     p.draw.rect(screen,GREEN,(400,475,180,100))

                                     p.draw.rect(screen,RED,(20,475,180,100))

                                     screen.blit(font2.render("Reset",True,WHITE),(50,505))

                                     screen.blit(font2.render("Check",True,WHITE),(430,505))

                                 else:

                                     cardsinhand=0

                                     screen.blit(checkmark,(262,560))

                             else:

                                 for i in range(0,3):

                                     if hand2[i]==[number,suit] or hand[i]==[number,suit]:

                                         already_clicked=True

                                 if not already_clicked: 

                                     hand2[cardsinhand]=[number,suit]

                                     p.draw.rect(screen,WHITE,(355,485+cardsinhand*35,140,27))

                                     screen.blit(font4.render(cardvalue[14-number],False,suitcol[suit-1]),(375,490+cardsinhand*35))

                                     p.draw.rect(screen,BLACK,((20+150*(suit-1)),(11+33*(math.floor((position[1]-11)/33))),110,26))

                                     if suit==1:

                                         screen.blit(heart,(455,486+cardsinhand*35))

                                     elif suit==2:

                                         screen.blit(club,(455,486+cardsinhand*35))

                                     elif suit==3:

                                         screen.blit(diamond,(455,486+cardsinhand*35))

                                     else:

                                         screen.blit(spade,(455,486+cardsinhand*35))

                                     cardsinhand+=1

                             if cardsinhand==3:

                                     p.draw.rect(screen,GREEN,(400,475,180,100))

                                     p.draw.rect(screen,RED,(20,475,180,100))

                                     screen.blit(font2.render("Reset",True,WHITE),(50,505))

                                     screen.blit(font2.render("Check",True,WHITE),(430,505))

                             p.display.update()

                else:

                    if 475<position[1]<575:

                        if 20<position[0]<200:

                            pokermenu(players)

                            hand=[[1,1],[1,1],[1,1]]

                            cardsinhand=0

                        elif 400<position[0]<580:

                            mode=3

                            tcp_showodds(win,lose,tie,noplay)

                            remove(carddeck,hand)

                            if players==2:

                                remove(carddeck,hand2)

                            dealercard(carddeck,hand,handdecide(hand),win,lose,tie,noplay)

                            hand=[[1,1],[1,1],[1,1]]

                           

            elif mode==3:

                if 100<position[0]<500 and 400<position[1]<580:

                    mode=0

                    cardsinhand=0

                    carddeck=([[14,1],[14,2],[14,3],[14,4],[13,1],[13,2],[13,3],[13,4],[12,1],[12,2],[12,3],[12,4],[11,1],[11,2],[11,3],[11,4],[10,1],[10,2],[10,3],[10,4],[9,1],[9,2],[9,3],[9,4],[8,1],[8,2],[8,3],[8,4],[7,1],[7,2],[7,3],[7,4],[6,1],[6,2],[6,3],[6,4],[5,1],[5,2],[5,3],[5,4],[4,1],[4,2],[4,3],[4,4],[3,1],[3,2],[3,3],[3,4],[2,1],[2,2],[2,3],[2,4]])

                    startmenu()

                            

        elif event.type == p.KEYDOWN:

            key=event.key

            if mode==1 or mode==-1:

                players=(int(key)-48)

                if 0<players<3:    

                    gamemenu()

                    screen.blit(title.render(str(players),False,WHITE),(233,300))

                    screen.blit(font4.render("Click anywhere to continue with this many players,",False,WHITE),(70,500))

                    screen.blit(font4.render("or enter a different number of players",False,WHITE),(130,550))

                    p.display.update()

                else:

                    screen.blit(font2.render("Please enter either 1 or 2",True,RED),(70,260))

                    p.display.update()

                    time.sleep(0.7)

                    gamemenu()

           

p.quit()