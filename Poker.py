from random import *
import tkinter.font as tkFont
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk

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
                image = s + str(v) + "jpg"
                deck.append(cards(s,v, image))
                shuffle(deck)
        
        self.p1.hand = [deck[0],deck[2]]
        self.p2.hand = [deck[1],deck[3]]
        self.board = [deck[4],deck[5],deck[6],deck[7],deck[8]]


p1 = player(input("Please input your name?"))
p2 = player(input("Please input your name?"))


# class main_screen(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         global font1
#         font1 = tkFont.Font(family = "Arial", size = 24)
#         button1 = tk.Button(self, text = "One Player", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue")
#         button1.grid(row = 1, column = 1)  
        

#         button2 = tk.Button(self, text = "Two Player", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue")
#         button2.grid(row = 3, column = 1)
#         self.columnconfigure(0,weight = 1)
#         self.columnconfigure(2,weight = 1)
#         self.rowconfigure(0,weight = 1)
#         self.rowconfigure(4,weight = 1)
#         self.rowconfigure(2,minsize = 20)
#         self.columnconfigure(0,minsize = 250)
#         self.columnconfigure(2,minsize = 250)
#         self.geometry("800x700")


        # c1 = tk.Canvas(self, width = 258, height = 181, bd = 0, highlightthickness = 0, bg = "tomato")  #This is the top middle image
        # c1.grid(row=0,column=1)
        # global poker
        # poker = ImageTk.PhotoImage(Image.open("Poker_image.png"))
        # c1.create_image(0,0,anchor="nw", image = poker)

        # c2 = tk.Canvas(self, width = 201, height = 201, bd = 0, highlightthickness = 0, bg = "tomato")  #This is the bottom left image
        # c2.grid(row=4,column=0)
        # global ace
        # ace = ImageTk.PhotoImage(Image.open("Poker_spade.png"))
        # c2.create_image(0,0,anchor="nw", image = ace)

#         Box = tk.Label(self, text = "Biggest pots won", font = font1, height = 3, width = 20, bg = "tomato") # This will list the largest 
#         Box.grid(column = 2, row = 0, sticky = "ne")                                                         # amount of money won in a hand

# class difficulty_screen(tk.Tk):
#      def __init__(self):
#         tk.Tk.__init__(self)
#         font1 = tkFont.Font(family = "Arial", size = 24)
        # button3 = tk.Button(self, text = "Easy", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue")
        # button3.grid(row = 1, column = 1)

#         button4 = tk.Button(self, text = "Hard", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue")
#         button4.grid(row = 3, column = 1)

        # Box = tk.Label(self, text = "Choose a difficulty", font = font1, height = 3, width = 20, bg = "tomato")
        # Box.grid(column = 1, row = 0, sticky = "nsew")

#         self.columnconfigure(0,weight = 1)
#         self.columnconfigure(2,weight = 1)
#         self.rowconfigure(0,weight = 1)
#         self.rowconfigure(4,weight = 1)
#         self.rowconfigure(2,minsize = 20)
#         self.columnconfigure(0,minsize = 250)
#         self.columnconfigure(2,minsize = 250)
#         self.geometry("800x700")

class main_screen(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        global font1                                                    #delete this when all windows made
        font1 = tkFont.Font(family = "Arial", size = 24)
        self.columnconfigure(0,weight = 1)
        #self.rowconfigure(0,weight = 1)
        self.columnconfigure(8,weight = 1)
        #self.rowconfigure(0,weight = 1)

        background = tk.Canvas(self, width = 820, height = 392, bd = 0, highlightthickness = 0, bg = "black")  #This is the top middle image
        background.grid(row=2,column=2, rowspan = 3, columnspan = 5)
        table = ImageTk.PhotoImage(Image.open("Poker_table.png"))
        background.create_image(0,0,anchor="nw", image = table)
        self.geometry("800x700")

        button_fold = tk.Button(self, text = "Fold", font = font1, height = 3, width = 12, highlightbackground = "tomato")
        button_fold.grid(row = 5, column = 2)

        button_check = tk.Button(self, text = "Check", font = font1, height = 3, width = 12, highlightbackground = "tomato")
        button_check.grid(row = 5, column = 3)

        button_call = tk.Button(self, text = "Call", font = font1, height = 3, width = 12, highlightbackground = "tomato")
        button_call.grid(row = 5, column = 4)

        button_bet = tk.Button(self, text = "Bet", font = font1, height = 3, width = 12, highlightbackground = "tomato")
        button_bet.grid(row = 5, column = 5)

        button_view1 = tk.Button(self, text = "View Cards", font = font1, height = 3, width = 12, highlightbackground = "tomato")
        button_view1.grid(row = 4, column = 0)

        button_view2 = tk.Button(self, text = "View Cards", font = font1, height = 3, width = 12, highlightbackground = "tomato")
        button_view2.grid(row = 4, column = 8)

        card1 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card1.grid(row=3,column=0)
        global back
        back = ImageTk.PhotoImage(Image.open("Red_back.jpg"))
        card1.create_image(0,0,anchor="nw", image = back)

        card2 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card2.grid(row=3,column=1)
        card2.create_image(0,0,anchor="nw", image = back)

        card3 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card3.grid(row=3,column=7)
        card3.create_image(0,0,anchor="nw", image = back)

        card4 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        card4.grid(row=3,column=8)
        card4.create_image(0,0,anchor="nw", image = back)

        name1 = tk.Label(self, text = p1.name, font = font1, fg = "yellow", height = 3, width = 20, bg = "black")
        name1.grid(column = 0, row = 0, sticky = "nsew")

        name2 = tk.Label(self, text = p2.name, font = font1, fg = "yellow", height = 3, width = 20, bg = "black")
        name2.grid(column = 8, row = 0, sticky = "nsew")

        money1 = tk.Label(self, text = p1.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
        money1.grid(column = 0, row = 1, sticky = "nsew")

        money2 = tk.Label(self, text = p2.money, font = font1, fg = "blue", height = 3, width = 20, bg = "black")
        money2.grid(column = 8, row = 1, sticky = "nsew")


        # card1 = tk.Canvas(self, width = 100, height = 152, bd = 0, highlightthickness = 0, bg = "black")  
        # card1.grid(row=3,column=0)
        # global back
        # back = ImageTk.PhotoImage(Image.open("Red_back.jpg"))
        # card1.create_image(0,0,anchor="nw", image = back)

        # board1 = ImageTk.PhotoImage(Image.open("Red_back.jpg"))
        # boardID = self.background.create_image(100,152,image = board1)

        # b1Image =  PhotoImage(file = "button1.png") 
        # b1ID = self.theCanvas.create_image(300,100,image=b1Image)  # Draw them on the canvas and remember their ID number

        # c1 = Canvas(master, width=50, height = 50)
        # c1.grid(row=1,column=1)
        # smiley = PhotoImage(file="smile.png")
        # c1.create_image(0,0,image=smiley,anchor="nw")



app = main_screen()

app.configure(bg = "black")

app.mainloop()







# newgame = game(0,p1,p2)
# print(newgame.board)
# print(newgame.p1.hand)
# print(newgame.p2.hand)


#def show(self, image):
    

#image = makeSprite("cards/7C.jpg")



#for card in deck:
 #   print(card.suit,card.value)    
    



#endWait()