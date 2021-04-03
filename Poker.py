from random import *
import tkinter.font as tkFont
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import time
import itertools
import pygame

class player:
    def __init__(self,name):
        self.hand = []            # in deal function add to this
        self.money = 1000
        self.name = name
        self.totalBet = 0


class cards:
    def __init__(self, suit, value, image):
        self.suit = suit
        self.value = value
        self.image = image

class game:
    def __init__(self,pot,p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.board = []     # add to this in deal function
        self.pot = 0        # this must be updated when bets are made
        self.deal()
    def deal(self):
        deck = []
        for s in ['D','C','H','S']:
            for v in range(2,15):
                image = str(v) + s + ".jpg"
                deck.append(cards(s,v, image))
                shuffle(deck)
        
        self.p1.hand = [deck[0],deck[1]]
        self.p2.hand = [deck[2],deck[3]]
        self.board = [deck[4],deck[5],deck[6],deck[7],deck[8]]



# p1 = player(input("Please input your name?"))
# p2 = player(input("Please input your name?"))
p1=player("Bob")
p2=player("Alice")
newgame = game(0,p1,p2)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1900x1000+0+0")
        self.title("Main Menu")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.loggedInUser = ""



        self.playerNum = None
        self.difficulty = 1     #easy   #if easy selected then leave this, else change to 2 to represent hard
        self.betStage = 0     # 0 is pre-flop, 1 means the flop has been done ... 
        self.playerGo = 1           #Tracks whos go it is
        self.handNum = 1            #Tracks which hand the game is on.
        self.maxBet = min(newgame.p1.money , newgame.p2.money)  #equal to the amount of money the player with the least has
        self.amount = 20              #current bet
        self.previousBet = 10        #Tracks the previous bet, so you can't bet less.
        self.AllIn = False          #Tracks if a player has gone all in
        self.smallBlind = 1         #Tracks who is small blind
        self.blindAllin = False
        newgame.p1.money = 990
        newgame.p1.totalBet = 10
        newgame.p2.money = 980
        newgame.p2.totalBet = 20
        newgame.pot = 30
        

        self.frames = {}

        for F in [main_screen, game_screen, difficulty_screen]:
            frame = F(self)
            self.frames[F] = frame

        self.show_frame(main_screen)

    def show_frame(self, cont):
        for frame in self.frames:
            self.frames[frame].grid_forget()
        frame = self.frames[cont]
        frame.grid(row=0, column=0, sticky="nsew")
        try:
            frame.loadup()
        except AttributeError:
            pass


class main_screen(tk.Frame):
    def __init__(self, controller):
        self.controller = controller
        tk.Frame.__init__(self,controller)
        global font1
        font1 = tkFont.Font(family = "Arial", size = 24)
        global font2
        font2 = tkFont.Font(family = "Arial", size = 18)
        self.config(bg="tomato")

        scores = open("scores.txt", "r")
        txt = ""
        for line in scores:
            txt += line
        txt = txt[:-1]
        scores.close()

        potWinners = tk.Label(self, text = txt, font = font1, fg = "black", height = 3, width = 20, bg = "tomato")
        potWinners.grid(column = 2, row = 1, sticky = "ne")

        button1 = tk.Button(self, text = "One Player", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = self.onePlayerStart)
        button1.grid(row = 2, column = 1)                                       
        #send you to selecting difficulty screen

        button2 = tk.Button(self, text = "Two Player", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = self.twoPlayerStart)
        # send you to the main game screen
        button2.grid(row = 4, column = 1)
        self.columnconfigure(0,weight = 1)
        self.columnconfigure(2,weight = 1)
        self.rowconfigure(0,weight = 1)
        self.rowconfigure(5,weight = 1)
        self.rowconfigure(3,minsize = 20)

        c1 = tk.Canvas(self, width = 258, height = 181, bd = 0, highlightthickness = 0, bg = "tomato")  #This is the top middle image
        c1.grid(row=0,column=1, rowspan = 2, sticky = "n")
        global poker
        poker = ImageTk.PhotoImage(Image.open("Poker_image.png"))
        c1.create_image(0,0,anchor="nw", image = poker)

        c2 = tk.Canvas(self, width = 201, height = 201, bd = 0, highlightthickness = 0, bg = "tomato")  #This is the bottom left image
        c2.grid(row=5,column=0)
        global ace
        ace = ImageTk.PhotoImage(Image.open("Poker_spade.png"))
        c2.create_image(0,0,anchor="nw", image = ace)

        Box = tk.Label(self, text = "Biggest pots won", font = font1, height = 3, width = 20, bg = "tomato") # This will list the largest 
        Box.grid(column = 2, row = 0, sticky = "ne")                                                         # amount of money won in a hand

    def onePlayerStart(self):
        self.controller.playerNum = 1 
        self.controller.show_frame(difficulty_screen)       #Called by the One player button

    
    def twoPlayerStart(self):
        self.controller.playerNum = 2 
        self.controller.show_frame(game_screen)             #Called by the Two player button


class difficulty_screen(tk.Frame):
    def __init__(self, controller):
        self.controller = controller
        tk.Frame.__init__(self,controller)
        self.config(bg="tomato")
        button3 = tk.Button(self, text = "Easy", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = lambda: self.controller.show_frame(game_screen))
        button3.grid(row = 1, column = 1)

        button4 = tk.Button(self, text = "Hard", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = self.hardBot)
        # lambda: [self.controller.show_frame(game_screen) , self.dSelect]) 
        button4.grid(row = 3, column = 1)                                                                                    #dSelect not being run

        Box = tk.Label(self, text = "Choose a difficulty", font = font1, height = 3, width = 20, bg = "tomato")
        Box.grid(column = 1, row = 0, sticky = "nsew")

        self.columnconfigure(0,weight = 1)
        self.columnconfigure(2,weight = 1)
        self.rowconfigure(0,weight = 1)
        self.rowconfigure(4,weight = 1)
        self.rowconfigure(2,minsize = 20)
        self.columnconfigure(0,minsize = 250)
        self.columnconfigure(2,minsize = 250)

    def hardBot(self):
        self.controller.difficulty = 2    #To use later when running the main game  
        self.controller.show_frame(game_screen)


class game_screen(tk.Frame):
    def __init__(self, controller):
        # This is run when the screen is created,
        # which is at the very start of runtime, before they have logged in
        self.controller = controller
        tk.Frame.__init__(self,controller)
        betfont =  tkFont.Font(family = "Arial", size = 24)
        self.config(bg="black")

        self.columnconfigure(0,weight = 1)     
        self.columnconfigure(8,weight = 1)
       
        self.background = tk.Canvas(self, width = 820, height = 392, bd = 0, highlightthickness = 0, bg = "black")  
        self.background.grid(row=3,column=2, rowspan = 2, columnspan = 5)
        global table                                                            #This is the background poker table
        table = ImageTk.PhotoImage(Image.open("Poker_table.png"))
        self.background.create_image(0,0,anchor="nw", image = table)

        button_fold = tk.Button(self, text = "Fold", font = font1, height = 3, width = 12, highlightbackground = "tomato", command = self.folded) 
        button_fold.grid(row = 5, column = 2)  #fold button

        button_check = tk.Button(self, text = "Check", font = font1, height = 3, width = 12, highlightbackground = "tomato", command = self.check)
        button_check.grid(row = 5, column = 3)  #check button

        button_call = tk.Button(self, text = "Call", font = font1, height = 3, width = 12, highlightbackground = "tomato", command = self.call) 
        button_call.grid(row = 5, column = 4)  #call button

        button_bet = tk.Button(self, text = "Bet", font = font1, height = 3, width = 12, highlightbackground = "tomato", command = self.betSize)
        button_bet.grid(row = 5, column = 5)            #bet button
        self.bet1 = tk.Entry(self,width=5, font=font1)
        self.button_confirm = tk.Button(self, text = "confirm", font = font1, highlightbackground = "tomato", command = self.confirmBet)

        button_view1 = tk.Button(self, text = "View Cards", font = font1, height = 3, width = 12, highlightbackground = "tomato", command = self.revealp1)
        button_view1.grid(row = 4, column = 0)      #view cards button on the left

        if self.controller.playerNum == 1:
            pass
        else:
            self.button_view2 = tk.Button(self, text = "View Cards", font = font1, height = 3, width = 12, highlightbackground = "tomato", command = self.revealp2)
            self.button_view2.grid(row = 4, column = 8)      #view cards button on the right



        self.card1 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        self.card1.grid(row=3,column=0)                                  #left players first card
        self.back = ImageTk.PhotoImage(Image.open("Red_back.jpg")) 
        self.card1.create_image(0,0,anchor="nw", image = self.back)

        self.card2 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        self.card2.grid(row=3,column=1)                                 #left players second card
        self.card2.create_image(0,0,anchor="nw", image = self.back)

        self.card3 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        self.card3.grid(row=3,column=7)                                #right players first card
        self.card3.create_image(0,0,anchor="nw", image = self.back)

        self.card4 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        self.card4.grid(row=3,column=8)                                #right players second card
        self.card4.create_image(0,0,anchor="nw", image = self.back)

        name1 = tk.Label(self, text = newgame.p1.name, font = font1, fg = "yellow", height = 3, width = 20, bg = "black")
        name1.grid(column = 0, row = 0, sticky = "nsew")          #left players name

        name2 = tk.Label(self, text = newgame.p2.name, font = font1, fg = "yellow", height = 3, width = 20, bg = "black")
        name2.grid(column = 8, row = 0, sticky = "nsew")          #right players name

        self.money1 = tk.Label(self, text = newgame.p1.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
        self.money1.grid(column = 0, row = 1, sticky = "nsew")         #left players money

        self.money2 = tk.Label(self, text = newgame.p2.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
        self.money2.grid(column = 8, row = 1, sticky = "nsew")         #right players money

        self.pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")
        self.pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")    #amount of money currently in the pot
        
        self.boardID1 = self.background.create_image(200,196,image = self.back)
        self.boardID2 = self.background.create_image(305,196,image = self.back)
        self.boardID3 = self.background.create_image(410,196,image = self.back)     #All the board cards
        self.boardID4 = self.background.create_image(515,196,image = self.back)
        self.boardID5 = self.background.create_image(620,196,image = self.back)

    def loadup(self):
        # This is run when the screen is displayed, not when it's created
        if self.controller.playerNum == 1:
            self.button_view2.grid_forget()

    def confirmBet(self):
        self.bet1.grid_forget()
        self.button_confirm.grid_forget() # hide the buttons

        if self.bet1.get().isdigit():
            amountCheck = int(self.bet1.get())

            if self.controller.playerGo == 1:
                if amountCheck > 0 and amountCheck <= self.controller.maxBet - newgame.p1.totalBet and amountCheck <= int(newgame.p1.money) and amountCheck > self.controller.previousBet:  
                    self.controller.amount = amountCheck
                    newgame.p1.totalBet += self.controller.amount
                    self.controller.previousBet = self.controller.amount  
                    newgame.pot += self.controller.amount
                    print("Player " + str(self.controller.playerGo) + " bet " + "£" + str(self.controller.amount))
                    self.pot_label.grid_forget()
                    self.pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")     #updating the pot label
                    self.pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")

                    self.controller.playerGo = 2        #so player 2 can act
                    newgame.p1.money -= self.controller.amount
                    self.money1.grid_forget()
                    self.money1 = tk.Label(self, text = newgame.p1.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
                    self.money1.grid(column = 0, row = 1, sticky = "nsew")              #updating the players money

                    if newgame.p1.totalBet == self.controller.maxBet:
                        self.controller.AllIn = True

                else:
                    self.betLabel = tk.Label(self, text = "Please enter a legal bet", font = font2, fg = "blue", height = 3, width = 20, bg = "black")
                    self.betLabel.grid(column = 8, row = 5, sticky = "nsew")
                    self.controller.after(2000, self.betLabelForget)

                    
            else:
                if amountCheck > 0 and amountCheck <= self.controller.maxBet - newgame.p2.totalBet and amountCheck <= int(newgame.p2.money) and amountCheck > self.controller.previousBet:
                    self.controller.amount = amountCheck
                    newgame.p2.totalBet += self.controller.amount
                    self.controller.previousBet = self.controller.amount
                    newgame.pot += self.controller.amount
                    print("Player " + str(self.controller.playerGo) + " bet " + "£" + str(self.controller.amount))
                    self.pot_label.grid_forget()
                    self.pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")     #updating the pot label
                    self.pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")

                    self.controller.playerGo = 1
                    newgame.p2.money -= self.controller.amount
                    self.money2.grid_forget()
                    self.money2 = tk.Label(self, text = newgame.p2.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
                    self.money2.grid(column = 8, row = 1, sticky = "nsew")              #updating the players money

                    if newgame.p2.totalBet == self.controller.maxBet:
                        self.controller.AllIn = True            
                
                else:
                    self.betLabel = tk.Label(self, text = "Please enter a legal bet", font = font2, fg = "blue", height = 3, width = 20, bg = "black")
                    self.betLabel.grid(column = 8, row = 5, sticky = "nsew")
                    self.controller.after(2000, self.betLabelForget)


        else:
            self.betLabel = tk.Label(self, text = "Please enter a legal bet", font = font2, fg = "blue", height = 3, width = 20, bg = "black")
            self.betLabel.grid(column = 8, row = 5, sticky = "nsew")
            self.controller.after(2000, self.betLabelForget)


    def betLabelForget(self):
        self.betLabel.grid_forget()


        
    def betSize(self):
        self.bet1.grid(row = 6, column = 5) # put the button and bet box on the grid
        self.button_confirm.grid(row = 8, column = 5)
        self.rowconfigure(7,minsize = 5)
        self.bet1.delete(0,"end") # clear box
        self.bet1.focus_set() # move cursor to the box

    def folded(self):
        self.bet1.grid_forget()
        self.button_confirm.grid_forget()
        print("Player " + str(self.controller.playerGo) + " folded")
        if self.controller.playerGo == 1:
            newgame.p2.money += newgame.pot
            self.newHand()    # Move onto next hand
        else:
            newgame.p1.money += newgame.pot
            self.newHand()    # Move onto next hand

    def newHand(self):

        print(" ")
        print("New Hand")
        print(" ")

        self.controller.blindAllin = False
        self.controller.handNum += 1
        game.deal(newgame)
        self.controller.betStage = 0
        self.controller.AllIn = False

        if self.controller.handNum % 2 == 0:
            self.controller.playerGo = 2
        else:
            self.controller.playerGo = 1

        self.boardID1 = self.background.create_image(200,196,image = self.back)
        self.boardID2 = self.background.create_image(305,196,image = self.back)
        self.boardID3 = self.background.create_image(410,196,image = self.back)
        self.boardID4 = self.background.create_image(515,196,image = self.back)
        self.boardID5 = self.background.create_image(620,196,image = self.back)

        self.card1.create_image(0,0,anchor="nw", image = self.back) 
        self.card2.create_image(0,0,anchor="nw", image = self.back)
        self.card3.create_image(0,0,anchor="nw", image = self.back)
        self.card4.create_image(0,0,anchor="nw", image = self.back)

        if newgame.p1.money == 0 or newgame.p2.money == 0:
            newgame.pot = 0

        elif self.controller.smallBlind == 1 and newgame.p1.money > 20 and newgame.p2.money > 10: #P1 was small blind, big blind now
            if newgame.p1.money > 20 and newgame.p2.money > 20:
                self.controller.smallBlind = 2
                newgame.p1.money -= 20
                newgame.p1.totalBet = 20
                newgame.p2.money -= 10                                                                  #Both players have enough money
                newgame.p2.totalBet = 10
                newgame.pot = 30
                self.controller.maxBet = min(newgame.p1.money , newgame.p2.money)
                self.controller.amount = 20
                self.controller.previousBet = 10
            else:
                self.controller.smallBlind = 2
                newgame.p1.money -= 20
                newgame.p1.totalBet = 20                                #Both players have enough money for blinds but p2 has < 20
                newgame.p2.money -= 10                                      
                newgame.p2.totalBet = 10
                newgame.pot = 30
                self.controller.blindAllin = True

        elif self.controller.smallBlind == 2 and newgame.p1.money > 10 and newgame.p2.money > 20:   #P1 was big blind, small blind now
            if newgame.p1.money > 20 and newgame.p2.money > 20:
                self.controller.smallBlind = 1
                newgame.p1.money -= 10
                newgame.p1.totalBet = 10                                                                #Both players have enough money
                newgame.p2.money -= 20
                newgame.p2.totalBet = 20
                newgame.pot = 30
                self.controller.maxBet = min(newgame.p1.money , newgame.p2.money)
                self.controller.amount = 20
                self.controller.previousBet = 10
            else:
                self.controller.smallBlind = 1
                newgame.p1.money -= 10
                newgame.p1.totalBet = 10                                   #Both players have enough money for blinds but p1 has < 20
                newgame.p2.money -= 20
                newgame.p2.totalBet = 20
                newgame.pot = 30
                self.controller.blindAllin = True
        
        elif self.controller.smallBlind == 2 and newgame.p1.money < 10:           #P1 is small blind, but does not have enough for this.
            self.controller.smallBlind = 1
            newgame.pot = int(newgame.p1.money) + 20
            newgame.p1.money = 0                            #Put all of P1 money into the pot and put the big blind from P2 into the pot, 
            newgame.p2.money -= 20                          # then call the all in function.
            self.controller.after(2000, self.allIn)
        
        elif self.controller.smallBlind == 2 and newgame.p2.money < 20:   #P1 is small blind and P2 does not have enough for the big blind.
            self.controller.smallBlind = 1
            newgame.pot = int(newgame.p2.money) + 10                      #Put the small blind in from P1, put all of P2’s money in the 
            if newgame.p2.money <= 10:                                    #pot, if this is less than the small blind then call the all in 
                self.controller.after(2000,self.allIn)                    # function, if it is more, check if P1 wants to call the 
            else:                                                         # additional money.
                newgame.p1.totalBet = 10
                newgame.p2.totalBet = newgame.p2.money
                self.controller.amount = newgame.p2.money
                self.controller.previousBet = 10

            newgame.p1.money -= 10
            newgame.p2.money = 0
        
        elif self.controller.smallBlind == 1 and newgame.p2.money < 10:           #P2 is small blind and does not have enough for this.
            self.controller.smallBlind = 2
            newgame.pot = int(newgame.p2.money) + 20                              #Put all of P2’s money into the pot and also put in the
            newgame.p1.money -= 20                                                #big blind from P1 then call the all in function.
            newgame.p2.money = 0
            self.controller.after(2000, self.allIn)
        
        elif self.controller.smallBlind == 1 and newgame.p1.money < 20:   #P2 is small blind and P1 does not have enough for the big blind
            self.controller.smallBlind = 2
            newgame.pot = int(newgame.p1.money) + 10                      #Put the small blind in from P2, then put in all of P1’s money,
            if newgame.p1.money <= 10:                                    #if this is less than the small blind then call the all in
                self.controller.after(2000, self.allIn)                   #function, if it is more, check if P2 wants to call the
            else:                                                         #additional money.
                newgame.p1.totalBet = newgame.p1.money
                newgame.p2.totalBet = 10
                self.controller.amount = newgame.p1.money
                self.controller.previousBet = 10

            newgame.p1.money = 0
            newgame.p2.money -= 10


        self.money1.grid_forget()
        self.money2.grid_forget()

        self.money1 = tk.Label(self, text = newgame.p1.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
        self.money2 = tk.Label(self, text = newgame.p2.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")

        #updating players money

        self.money1.grid(column = 0, row = 1, sticky = "nsew")
        self.money2.grid(column = 8, row = 1, sticky = "nsew")

        self.pot_label.grid_forget()
        self.pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")     #updating the pot label
        self.pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")




        #newgame.pot = 0
        #self.controller.maxBet = min(newgame.p1.money , newgame.p2.money)
        #self.controller.amount = None
        #self.controller.previousBet = 0
        #newgame.p1.totalBet = 0
        #newgame.p2.totalBet = 0






    def call(self):
        self.bet1.grid_forget()
        self.button_confirm.grid_forget()
        if self.controller.blindAllin == True:
            if self.controller.smallBlind == 1:
                newgame.pot += newgame.p1.money
                newgame.p1.money = 0

                self.money1.grid_forget()
                self.money1 = tk.Label(self, text = newgame.p1.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
                self.money1.grid(column = 0, row = 1, sticky = "nsew")      #updating players money

                self.pot_label.grid_forget()
                self.pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")
                self.pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")       #updating the pot label

                self.allIn()

            if self.controller.smallBlind == 2:
                newgame.pot += newgame.p2.money
                newgame.p2.money = 0
                self.money2.grid_forget()
                self.money2 = tk.Label(self, text = newgame.p2.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
                self.money2.grid(column = 8, row = 1, sticky = "nsew")      #updating players money

                self.pot_label.grid_forget()
                self.pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")
                self.pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")       #updating the pot label

                self.allIn()

        else:
            if self.controller.amount is None:
                self.callLabel = tk.Label(self, text = "No bet has been made", font = font2, fg = "blue", height = 3, width = 20, bg = "black")
                self.callLabel.grid(column = 8, row = 5, sticky = "nsew")
                self.controller.after(2000, self.callLabelForget)

            else:
                print("Player " + str(self.controller.playerGo) + " called")

                if self.controller.playerGo == 1 and self.controller.handNum % 2 == 0:  
                    
                    newgame.pot += newgame.p2.totalBet - newgame.p1.totalBet
                    self.pot_label.grid_forget()
                    self.pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")     #updating the pot label
                    self.pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")


                    self.controller.playerGo = 2        #so player 2 can act
                    newgame.p1.money -= newgame.p2.totalBet - newgame.p1.totalBet
                    self.money1.grid_forget()
                    self.money1 = tk.Label(self, text = newgame.p1.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
                    self.money1.grid(column = 0, row = 1, sticky = "nsew")              #updating the players money


                elif self.controller.playerGo == 1 and self.controller.handNum % 2 == 1:    
                    
                    newgame.pot += newgame.p2.totalBet - newgame.p1.totalBet
                    self.pot_label.grid_forget()
                    self.pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")     #updating the pot label
                    self.pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")

                    # player 1 acts first in next round so dont change playerGo
                    newgame.p1.money -= newgame.p2.totalBet - newgame.p1.totalBet
                    self.money1.grid_forget()
                    self.money1 = tk.Label(self, text = newgame.p1.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
                    self.money1.grid(column = 0, row = 1, sticky = "nsew")              #updating the players money


                elif self.controller.playerGo == 2 and self.controller.handNum % 2 == 1:    

                    newgame.pot += newgame.p1.totalBet - newgame.p2.totalBet
                    self.pot_label.grid_forget()
                    self.pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")     #updating the pot label
                    self.pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")

                    self.controller.playerGo = 1
                    newgame.p2.money -= newgame.p1.totalBet - newgame.p2.totalBet
                    self.money2.grid_forget()
                    self.money2 = tk.Label(self, text = newgame.p2.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
                    self.money2.grid(column = 8, row = 1, sticky = "nsew")              #updating the players money


                elif self.controller.playerGo == 2 and self.controller.handNum % 2 == 0:
                    
                    newgame.pot += newgame.p1.totalBet - newgame.p2.totalBet
                    self.pot_label.grid_forget()
                    self.pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")     #updating the pot label
                    self.pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")

                    #player 2 acts first next round so dont change back to player 1 go.

                    newgame.p2.money -= newgame.p1.totalBet - newgame.p2.totalBet
                    self.money2.grid_forget()
                    self.money2 = tk.Label(self, text = newgame.p2.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
                    self.money2.grid(column = 8, row = 1, sticky = "nsew")              #updating the players money

                if self.controller.AllIn == True:
                    self.allIn()  
                elif self.controller.betStage == 0:
                    self.flop()
                elif self.controller.betStage == 1:                                     # figures out which round and show cards
                    self.turn()
                elif self.controller.betStage == 2:
                    self.river()
                else:
                    self.compare()                            #compare the 2 players hands and output a winner


    def callLabelForget(self):
        self.callLabel.grid_forget()    


    def check(self):
        self.bet1.grid_forget()
        self.button_confirm.grid_forget()
        if self.controller.amount == None:
            print("Player " + str(self.controller.playerGo) + " checked")
            if self.controller.playerGo == 1 and self.controller.handNum % 2 == 1:  # if is is player 1 and they are going first
                self.controller.playerGo = 2

            elif self.controller.playerGo == 1 and self.controller.handNum % 2 == 0:  # if is is player 1 and they are going second 
                self.controller.playerGo = 2                                          # - ie betting round over
  
                if self.controller.betStage == 0:
                    self.flop()
                elif self.controller.betStage == 1:                                     # figures out which round and show cards
                    self.turn()
                elif self.controller.betStage == 2:
                    self.river()
                else:
                    self.compare()                            #compare the 2 players hands and output a winner

            elif self.controller.playerGo == 2 and self.controller.handNum % 2 == 0:    #player twos go and they are acting first
                self.controller.playerGo = 1

            elif self.controller.playerGo == 2 and self.controller.handNum %2 == 1:     #player twos go and they are acting second
                self.controller.playerGo = 1
                if self.controller.betStage == 0:
                    self.flop()
                elif self.controller.betStage == 1:
                    self.turn()
                elif self.controller.betStage == 2:
                    self.river()
                else:
                    self.compare()                            #compare the 2 players hands and output a winner
        
        else:
            self.checkLabel = tk.Label(self, text = "A bet has been made", font = font2, fg = "blue", height = 3, width = 20, bg = "black")
            self.checkLabel.grid(column = 8, row = 5, sticky = "nsew")
            self.controller.after(2000, self.hideCheckLabel)

    def hideCheckLabel(self):               #hide the label if player tries to check when a bet has been made
        self.checkLabel.grid_forget()


    def getValue(self,card):        #to use for the sort command in rank
        return card.value


    def rank(self,playerHand,board):
        allCards = []
        for i in playerHand:
            allCards.append(i)
        for i in board:
            allCards.append(i)
        allCards.sort(key=self.getValue)
        combination = itertools.combinations(allCards,5)
        highestScore = [0,0]    #value to compare each combination against
        for x in combination:
            currentScore = self.score(x)        #score of the current 5 card combination
            if highestScore[0] < currentScore[0]:   
                for i in range(2):
                    highestScore[i] = currentScore[i]   #setting highestScore to be currentScore
            elif highestScore[0] == currentScore[0] and highestScore[1] < currentScore[1]:
                for i in range(2):
                    highestScore[i] = currentScore[i]   #setting highestScore to be currentScore
        return highestScore
    

    def score(self,set):
        straight1 = False
        straight2 = False
        flush = False

        if set[0].value == set[1].value - 1 == set[2].value - 2 == set[3].value - 3 == set[4].value - 4:
            straight1 = True

        if set[0].value == set[1].value - 1 == set[2].value - 2 == set[3].value - 3 == set[4].value - 12:
            straight2 = True

        if set[0].suit == set[1].suit == set[2].suit == set[3].suit == set[4].suit:
            flush = True

        #Royal Flush
        if straight1 and flush and set[4].value == 14:
            return [9,0]

        #Straight Flush
        elif straight1 and flush:
            return [8,set[4].value]
        elif straight2 and flush:
            return [8,set[3].value]

        #Four of a kind
        elif set[4].value == set[3].value == set[2].value == set[1].value:
            return [7,(set[4].value)*10 + set[0].value]
        elif set[3].value == set[2].value == set[1].value == set[0].value:
            return [7,(set[3].value)*10 + set[4].value]

        #Full House
        elif set[4].value == set[3].value == set[2].value and set[1].value == set[0].value:
            return [6,(set[4].value)* 10 + set[1].value]
        elif set[2].value == set[1].value == set[0].value and set[4].value == set[3].value:
            return [6,(set[2].value)* 10 + set[4].value]
        
        #Flush
        elif flush:
            return[5,(set[4].value)* 10000 + (set[3].value)* 1000 + (set[2].value)*100 + (set[1].value)* 10 + (set[0].value)]
        
        #Straight
        elif straight1:
            return[4,set[4].value]
        elif straight2:
            return[4, set[3].value]
        
        #Three of a kind
        elif set[4].value == set[3].value == set[2].value:
            return[3,(set[4].value)* 100 + (set[1].value)* 10 + (set[0].value)]
        elif set[3].value == set[2].value == set[1].value:
            return[3,(set[3].value)* 100 + (set[4].value)* 10 + (set[0].value)]
        elif set[2].value == set[1].value == set[0].value:
            return[3,(set[2].value)* 100 + (set[4].value)* 10 + (set[3].value)]
        
        #Two Pair
        elif set[4].value == set[3].value and set[2].value == set[1].value:
            return[2, (set[4].value)* 100 + (set[2].value)*10 + set[0].value]
        elif set[4].value == set[3].value and set[1].value == set[0].value:
            return[2, (set[4].value)* 100 + (set[1].value)*10 + set[2].value]
        elif set[3].value == set[2].value and set[1].value == set[0].value:
            return[2, (set[3].value)* 100 + (set[1].value)*10 + set[4].value]
        
        #One Pair
        elif set[4].value == set[3].value:
            return[1,(set[4].value)* 1000 + (set[2].value)* 100 + (set[1].value)*10 + (set[0].value)]
        elif set[3].value == set[2].value:
            return[1,(set[3].value)* 1000 + (set[4].value)* 100 + (set[1].value)*10 + (set[0].value)]
        elif set[2].value == set[1].value:
            return[1,(set[2].value)* 1000 + (set[4].value)* 100 + (set[3].value)*10 + (set[0].value)]
        elif set[1].value == set[0].value:
            return[1,(set[1].value)* 1000 + (set[4].value)* 100 + (set[3].value)*10 + (set[2].value)]
        
        #High Card
        else:
            return [0,(set[4].value)* 10000 + (set[3].value)* 1000 + (set[2].value)*100 + (set[1].value)* 10 + set[0].value]



    def compare(self):
        p1Score = self.rank(newgame.p1.hand, newgame.board)
        p2Score = self.rank(newgame.p2.hand, newgame.board)
        if p1Score[0] > p2Score[0]:                             #P1 wins
            self.win1_label = tk.Label(self, text = str(newgame.p1.name) + " won the hand", font = font1, fg = "yellow", bg = "black")
            self.win1_label.grid(column = 3, row = 0, columnspan = 2, sticky = "nsew")
            newgame.p1.money += newgame.pot


            infile = open('scores.txt','r')
            newScore = '4. {} - £{}\n'.format(newgame.p1.name,newgame.pot)
            arr = []
            arr.append(newScore[:-1].split())
            for line in infile:
                arr.append(line[:-1].split())
            infile.close()
            outfile = open('scores.txt','w')

            arr.sort(key = lambda x: int(x[3][1:]),reverse=True)            
            for i in range(3):
                outfile.write('{}. {} - {}\n'.format(i+1,arr[i][1],arr[i][3]))

            outfile.close()

            self.controller.after(2000, self.hideWin1Label)

        elif p1Score[0] == p2Score[0] and p1Score[1] > p2Score[1]:      #P1 wins
            self.win1_label = tk.Label(self, text = str(newgame.p1.name)+ " won the hand", font = font1, fg = "yellow", bg = "black")
            self.win1_label.grid(column = 3, row = 0, columnspan = 2, sticky = "nsew")
            newgame.p1.money += newgame.pot

            infile = open('scores.txt','r')
            newScore = '4. {} - £{}\n'.format(newgame.p1.name,newgame.pot)
            arr = []
            arr.append(newScore[:-1].split())
            for line in infile:
                arr.append(line[:-1].split())
            infile.close()
            outfile = open('scores.txt','w')

            arr.sort(key = lambda x: int(x[3][1:]),reverse=True)            
            for i in range(3):
                outfile.write('{}. {} - {}\n'.format(i+1,arr[i][1],arr[i][3]))

            outfile.close()

            self.controller.after(2000, self.hideWin1Label)
       
        elif p1Score == p2Score:                                #Draw
            self.draw_label = tk.Label(self, text = "The hand was a draw", font = font1, fg = "yellow", bg = "black")
            self.draw_label.grid(column = 3, row = 0, columnspan = 2, sticky = "nsew")
            newgame.p1.money += newgame.pot // 2
            newgame.p2.money += newgame.pot // 2

            self.controller.after(2000, self.hideDrawLabel)
        else:                                                         #P2 wins
            self.win2_label = tk.Label(self, text = str(newgame.p2.name) + " won the hand", font = font1, fg = "yellow", bg = "black")
            self.win2_label.grid(column = 3, row = 0, columnspan = 2, sticky = "nsew")
            newgame.p2.money += newgame.pot

            infile = open('scores.txt','r')
            newScore = '4. {} - £{}\n'.format(newgame.p2.name,newgame.pot)
            arr = []
            arr.append(newScore[:-1].split())
            for line in infile:
                arr.append(line[:-1].split())
            infile.close()
            outfile = open('scores.txt','w')

            arr.sort(key = lambda x: int(x[3][1:]),reverse=True)            
            for i in range(3):
                outfile.write('{}. {} - {}\n'.format(i+1,arr[i][1],arr[i][3]))

            outfile.close()


            self.controller.after(2000, self.hideWin2Label)
        
        self.winner()
        self.newHand()


    def hideWin1Label(self):               #hide the  player 1 wins label 
        self.win1_label.grid_forget()

    def hideDrawLabel(self):               #hide the players have drawn label
        self.draw_label.grid_forget()

    def hideWin2Label(self):               #hide the  player 2 wins label
        self.win2_label.grid_forget()


    def allIn(self):
        if self.controller.betStage == 0:
            self.flop()
            self.turn()
            self.river()
            self.revealp1()
            self.revealp2()
        elif self.controller.betStage == 1:
            self.turn()
            self.river()
            self.revealp1()
            self.revealp2()
        elif self.controller.betStage == 2:
            self.river()
            self.revealp1()
            self.revealp2()
        elif self.controller.betStage == 3:
            self.revealp1()
            self.revealp2()

        self.controller.after(3000, self.compare)

    
    def winner(self):
        if newgame.p1.money == 0:
            self.winner2_label = tk.Label(self, text = str(newgame.p2.name) + " has won the game!", font = font1, fg = "yellow", bg = "black")
            self.winner2_label.grid(column = 3, row = 0, columnspan = 2, sticky = "nsew")
            self.controller.after(3000, self.end)
        elif newgame.p2.money == 0:
            self.winner1_label = tk.Label(self, text = str(newgame.p1.name) + " has won the game!", font = font1, fg = "yellow", bg = "black")
            self.winner1_label.grid(column = 3, row = 0, columnspan = 2, sticky = "nsew")
            self.controller.after(3000, self.end)


    def end(self):
        exit()


    def revealp1(self):
        self.p1cardimage1 = ImageTk.PhotoImage(Image.open(newgame.p1.hand[0].image))    #show right players cards
        self.card1.create_image(0,0,anchor="nw", image = self.p1cardimage1)

        self.p1cardimage2 = ImageTk.PhotoImage(Image.open(newgame.p1.hand[1].image))
        self.card2.create_image(0,0,anchor="nw", image = self.p1cardimage2)

        self.controller.after(3000, self.hideCards)


    def revealp2(self):

        self.p2cardimage1 = ImageTk.PhotoImage(Image.open(newgame.p2.hand[0].image))    #show right players cards
        self.card3.create_image(0,0,anchor="nw", image = self.p2cardimage1)

        self.p2cardimage2 = ImageTk.PhotoImage(Image.open(newgame.p2.hand[1].image))
        self.card4.create_image(0,0,anchor="nw", image = self.p2cardimage2)

        self.controller.after(3000, self.hideCards)

    def hideCards(self):
        self.card1.create_image(0,0,anchor="nw", image = self.back) 
        self.card2.create_image(0,0,anchor="nw", image = self.back)
        self.card3.create_image(0,0,anchor="nw", image = self.back)
        self.card4.create_image(0,0,anchor="nw", image = self.back)

    def flop(self):

        print(" ")
        print("Flop")
        print(" ")

        global board1                                               
        board1 = ImageTk.PhotoImage(Image.open(newgame.board[0].image))
        self.boardID1 = self.background.create_image(200,196,image = board1)

        global board2                                               
        board2 = ImageTk.PhotoImage(Image.open(newgame.board[1].image))
        self.boardID2 = self.background.create_image(305,196,image = board2)

        global board3                                           
        board3 = ImageTk.PhotoImage(Image.open(newgame.board[2].image))
        self.boardID3 = self.background.create_image(410,196,image = board3)

        self.controller.betStage = 1
        self.controller.amount = None
        newgame.p1.totalBet = 0
        newgame.p2.totalBet = 0
        self.controller.previousBet = 0
        self.controller.maxBet = min(newgame.p1.money , newgame.p2.money)
        




    def turn(self):

        print(" ")
        print("Turn")
        print(" ")

        global board4                                               
        board4 = ImageTk.PhotoImage(Image.open(newgame.board[3].image))
        self.boardID4 = self.background.create_image(515,196,image = board4)
        self.controller.betStage = 2
        self.controller.amount = None
        newgame.p1.totalBet = 0
        newgame.p2.totalBet = 0
        self.controller.previousBet = 0
        self.controller.maxBet = min(newgame.p1.money , newgame.p2.money)



    def river(self):

        print(" ")
        print("River")
        print(" ")

        global board5                                               
        board5 = ImageTk.PhotoImage(Image.open(newgame.board[4].image))
        self.boardID5 = self.background.create_image(620,196,image = board5)
        self.controller.betStage = 3
        self.controller.amount = None
        newgame.p1.totalBet = 0
        newgame.p2.totalBet = 0
        self.controller.previousBet = 0
        self.controller.maxBet = min(newgame.p1.money , newgame.p2.money)


app = App()

app.mainloop()