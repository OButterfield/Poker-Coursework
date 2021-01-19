from random import *
import tkinter.font as tkFont
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import time


playerNum = 2    #If two player selected then leave this, else change to one
difficulty = 1   #if easy selected then leave this, else change to 2 to represent hard
betStage = 0     # 0 is pre-flop, 1 means the flop has been done ... 


class player:
    def __init__(self,name):
        self.hand = []            # in deal function add to this
        self.money = 1000
        self.name = name


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


class main_screen(tk.Frame):
    def __init__(self, controller):
        self.controller = controller
        tk.Frame.__init__(self,controller)
        global font1
        font1 = tkFont.Font(family = "Arial", size = 24)
        self.config(bg="tomato")

        scores = open("scores.txt", "r")
        
        txt = ""
        for line in scores:
            txt += line

        scores.close()

        potWinners = tk.Label(self, text = txt, font = font1, fg = "black", height = 3, width = 20, bg = "tomato")
        potWinners.grid(column = 2, row = 1, sticky = "ne")

        button1 = tk.Button(self, text = "One Player", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = self.compound)
        button1.grid(row = 2, column = 1)                                       #numPlayers not being run
        #send you to selecting difficulty screen

        button2 = tk.Button(self, text = "Two Player", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = lambda: self.controller.show_frame(game_screen))
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

    def compound():
        playerNum = 1
        controller.show_frame(difficulty_screen)

    # def numPlayers():
    #     playerNum = 1   #not being run
        

class difficulty_screen(tk.Frame):
    def __init__(self, controller):
        self.controller = controller
        tk.Frame.__init__(self,controller)
        self.config(bg="tomato")
        button3 = tk.Button(self, text = "Easy", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = lambda: self.controller.show_frame(game_screen))
        button3.grid(row = 1, column = 1)

        button4 = tk.Button(self, text = "Hard", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = lambda: [self.controller.show_frame(game_screen) , self.dSelect]) 
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

    def dSelect():
        difficulty = 2    #To use later when running the main game


class game_screen(tk.Frame):
    def __init__(self, controller):
        self.controller = controller
        tk.Frame.__init__(self,controller)
        betfont =  tkFont.Font(family = "Arial", size = 24)
        self.config(bg="black")

        self.columnconfigure(0,weight = 1)     
        self.columnconfigure(8,weight = 1)
       
        self.background = tk.Canvas(self, width = 820, height = 392, bd = 0, highlightthickness = 0, bg = "black")  #This is the top middle image
        self.background.grid(row=3,column=2, rowspan = 2, columnspan = 5)
        global table
        table = ImageTk.PhotoImage(Image.open("Poker_table.png"))
        self.background.create_image(0,0,anchor="nw", image = table)

        button_fold = tk.Button(self, text = "Fold", font = font1, height = 3, width = 12, highlightbackground = "tomato") 
        button_fold.grid(row = 5, column = 2)  #fold button

        button_check = tk.Button(self, text = "Check", font = font1, height = 3, width = 12, highlightbackground = "tomato")
        button_check.grid(row = 5, column = 3)  #check button

        button_call = tk.Button(self, text = "Call", font = font1, height = 3, width = 12, highlightbackground = "tomato") #to test
        button_call.grid(row = 5, column = 4)  #call button

        button_bet = tk.Button(self, text = "Bet", font = font1, height = 3, width = 12, highlightbackground = "tomato", command = self.betSize)
        button_bet.grid(row = 5, column = 5)            #bet button
        self.bet1 = tk.Entry(self,width=5, font=font1)
        self.button_confirm = tk.Button(self, text = "confirm", font = font1, highlightbackground = "tomato", command = self.confirmBet)

        button_view1 = tk.Button(self, text = "View Cards", font = font1, height = 3, width = 12, highlightbackground = "tomato", command = self.revealp1)
        button_view1.grid(row = 4, column = 0)      #view cards button on the left

        self.button_view2 = tk.Button(self, text = "View Cards", font = font1, height = 3, width = 12, highlightbackground = "tomato", command = self.revealp2)
        self.button_view2.grid(row = 4, column = 8)      #view cards button on the right

        if playerNum == 1:
            self.button_view2.grid_forget()

        card1 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card1.grid(row=3,column=0)
        global back                                                 #left players first card
        back = ImageTk.PhotoImage(Image.open("Red_back.jpg"))
        card1.create_image(0,0,anchor="nw", image = back)

        card2 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card2.grid(row=3,column=1)                                 #left players second card
        card2.create_image(0,0,anchor="nw", image = back)

        card3 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card3.grid(row=3,column=7)                                #right players first card
        card3.create_image(0,0,anchor="nw", image = back)

        card4 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card4.grid(row=3,column=8)                                #right players second card
        card4.create_image(0,0,anchor="nw", image = back)

        name1 = tk.Label(self, text = p1.name, font = font1, fg = "yellow", height = 3, width = 20, bg = "black")
        name1.grid(column = 0, row = 0, sticky = "nsew")          #left players name

        name2 = tk.Label(self, text = p2.name, font = font1, fg = "yellow", height = 3, width = 20, bg = "black")
        name2.grid(column = 8, row = 0, sticky = "nsew")          #right players name

        money1 = tk.Label(self, text = p1.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
        money1.grid(column = 0, row = 1, sticky = "nsew")         #left players money

        money2 = tk.Label(self, text = p2.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
        money2.grid(column = 8, row = 1, sticky = "nsew")         #right players money

        pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")
        pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")    #amount of money currently in the pot
        
        self.boardID1 = self.background.create_image(200,196,image = back)
        self.boardID2 = self.background.create_image(305,196,image = back)
        self.boardID3 = self.background.create_image(410,196,image = back)      #cards on the board
        self.boardID4 = self.background.create_image(515,196,image = back)
        self.boardID5 = self.background.create_image(620,196,image = back)


    def confirmBet(self):
        self.bet1.grid_forget()
        self.button_confirm.grid_forget() # hide the buttons
        '''
        amount = int(self.bet1.get())
        if amount > 0:
            pot += amount
            #minus from player money
        else:
            betLabel = tk.Label(self, text = "Please enter a legal bet", font = font1, fg = "blue", height = 3, width = 20, bg = "black")
            betLabel.grid(column = 8, row = 5, sticky = "nsew")
        '''
        
    def betSize(self):
        self.bet1.grid(row = 6, column = 5) # put the button and bet box on the grid
        self.button_confirm.grid(row = 8, column = 5)
        self.rowconfigure(7,minsize = 5)
        self.bet1.delete(0,"end") # clear box
        self.bet1.focus_set() # move cursor to the box

    def revealp1(self):
        p1card1 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  # this layers multiple canvas on top of each other
        p1card1.grid(row=3,column=0)                                                                        #needs to be fixed
        global p1cardimage1
        p1cardimage1 = ImageTk.PhotoImage(Image.open(newgame.p1.hand[0].image))                                 #show right players cards
        p1card1.create_image(0,0,anchor="nw", image = p1cardimage1)

        p1card2 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        p1card2.grid(row=3,column=1)
        global p1cardimage2
        p1cardimage2 = ImageTk.PhotoImage(Image.open(newgame.p1.hand[1].image))
        p1card2.create_image(0,0,anchor="nw", image = p1cardimage2)

        app.update()

        time.sleep(1.5)

        card1 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card1.grid(row=3,column=0)
        card1.create_image(0,0,anchor="nw", image = back) 

        card2 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card2.grid(row=3,column=1)
        card2.create_image(0,0,anchor="nw", image = back)   

    def revealp2(self):
        p2card1 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        p2card1.grid(row=3,column=7)
        global p2cardimage1
        p2cardimage1 = ImageTk.PhotoImage(Image.open(newgame.p2.hand[0].image))                                 #show right players cards
        p2card1.create_image(0,0,anchor="nw", image = p2cardimage1)

        p2card2 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        p2card2.grid(row=3,column=8)
        global p2cardimage2
        p2cardimage2 = ImageTk.PhotoImage(Image.open(newgame.p2.hand[1].image))
        p2card2.create_image(0,0,anchor="nw", image = p2cardimage2)

        app.update()

        time.sleep(1.5)

        card3 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card3.grid(row=3,column=7)
        card3.create_image(0,0,anchor="nw", image = back) 

        card4 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card4.grid(row=3,column=8)
        card4.create_image(0,0,anchor="nw", image = back)   

    def flop(self):
        global board1                                               
        board1 = ImageTk.PhotoImage(Image.open(newgame.board[0].image))
        self.boardID1 = self.background.create_image(200,196,image = board1)

        global board2                                               
        board2 = ImageTk.PhotoImage(Image.open(newgame.board[1].image))
        self.boardID2 = self.background.create_image(305,196,image = board2)

        global board3                                           
        board3 = ImageTk.PhotoImage(Image.open(newgame.board[2].image))
        self.boardID3 = self.background.create_image(410,196,image = board3)

        betStage = 1


    def turn(self):
        global board4                                               
        board4 = ImageTk.PhotoImage(Image.open(newgame.board[3].image))
        self.boardID4 = self.background.create_image(515,196,image = board4)

        betStage = 2

    def river(self):
        global board5                                               
        board5 = ImageTk.PhotoImage(Image.open(newgame.board[4].image))
        self.boardID5 = self.background.create_image(620,196,image = board5)

        betStage = 3


    # def betSize():
    #     cover_button.grid_forget()


        # self.bet1 = tk.Entry()
        # self.bet1.grid(row = 5, column = 6, sticky = "s")
        # button_confirm = tk.Button(self, text = "confirm", font = font1, height = 3, width = 12, highlightbackground = "tomato", command = confirmBet)
        # button_confirm.grid(row = 5, column = 7)


app = App()

app.mainloop()


#print(newgame.board)
# print(newgame.p1.hand)
# print(newgame.p2.hand)


#def show(self, image):
    

#image = makeSprite("cards/7C.jpg")



#for card in deck:
 #   print(card.suit,card.value)    
    



#endWait()
