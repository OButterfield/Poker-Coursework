from random import *
import tkinter.font as tkFont
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk


playerNum = 2    #If two player selected then leave this, else change to one
difficulty = 1   #if easy selected then leave this, else change to 2 to represent hard


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
                image = s + str(v) + ".jpg"
                deck.append(cards(s,v, image))
                shuffle(deck)
        
        self.p1.hand = [deck[0],deck[2]]
        self.p2.hand = [deck[1],deck[3]]
        self.board = [deck[4],deck[5],deck[6],deck[7],deck[8]]




# p1 = player(input("Please input your name?"))
# p2 = player(input("Please input your name?"))
p1=player("a")
p2=player("b")
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

        #def numPlayers():      
            #playerNum = 1
        button1 = tk.Button(self, text = "One Player", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = lambda: self.controller.show_frame(difficulty_screen))#, command = numPlayers)
        button1.grid(row = 1, column = 1)  
        #send you to selecting difficulty screen

        button2 = tk.Button(self, text = "Two Player", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = lambda: self.controller.show_frame(game_screen))
        # send you to the main game screen
        button2.grid(row = 3, column = 1)
        self.columnconfigure(0,weight = 1)
        self.columnconfigure(2,weight = 1)
        self.rowconfigure(0,weight = 1)
        self.rowconfigure(4,weight = 1)
        self.rowconfigure(2,minsize = 20)
        # self.columnconfigure(0,minsize = 250)
        # self.columnconfigure(2,minsize = 250)



        c1 = tk.Canvas(self, width = 258, height = 181, bd = 0, highlightthickness = 0, bg = "tomato")  #This is the top middle image
        c1.grid(row=0,column=1)
        global poker
        poker = ImageTk.PhotoImage(Image.open("Poker_image.png"))
        c1.create_image(0,0,anchor="nw", image = poker)

        c2 = tk.Canvas(self, width = 201, height = 201, bd = 0, highlightthickness = 0, bg = "tomato")  #This is the bottom left image
        c2.grid(row=4,column=0)
        global ace
        ace = ImageTk.PhotoImage(Image.open("Poker_spade.png"))
        c2.create_image(0,0,anchor="nw", image = ace)

        Box = tk.Label(self, text = "Biggest pots won", font = font1, height = 3, width = 20, bg = "tomato") # This will list the largest 
        Box.grid(column = 2, row = 0, sticky = "ne")                                                         # amount of money won in a hand


class difficulty_screen(tk.Frame):
    def __init__(self, controller):
        self.controller = controller
        tk.Frame.__init__(self,controller)
        self.config(bg="tomato")
        button3 = tk.Button(self, text = "Easy", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = lambda: self.controller.show_frame(game_screen))
        button3.grid(row = 1, column = 1)

        #def dSelect():
        #    difficulty = 2      

        button4 = tk.Button(self, text = "Hard", font = font1, height = 3, width = 12, highlightbackground = "cornflower blue", command = lambda: self.controller.show_frame(game_screen))#, command = dSelect)
        button4.grid(row = 3, column = 1)

        Box = tk.Label(self, text = "Choose a difficulty", font = font1, height = 3, width = 20, bg = "tomato")
        Box.grid(column = 1, row = 0, sticky = "nsew")

        self.columnconfigure(0,weight = 1)
        self.columnconfigure(2,weight = 1)
        self.rowconfigure(0,weight = 1)
        self.rowconfigure(4,weight = 1)
        self.rowconfigure(2,minsize = 20)
        self.columnconfigure(0,minsize = 250)
        self.columnconfigure(2,minsize = 250)


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
        button_fold.grid(row = 5, column = 2)

        button_check = tk.Button(self, text = "Check", font = font1, height = 3, width = 12, highlightbackground = "tomato")
        button_check.grid(row = 5, column = 3)

        button_call = tk.Button(self, text = "Call", font = font1, height = 3, width = 12, highlightbackground = "tomato")
        button_call.grid(row = 5, column = 4)

        # cover_button = tk.button(self, height = 3, width = 12, highlightbackground = "black")
        # cover_button.grid(row = 5 , column = 6, columnspan = 2)


        button_bet = tk.Button(self, text = "Bet", font = font1, height = 3, width = 12, highlightbackground = "tomato", command = self.betSize)
        button_bet.grid(row = 5, column = 5, columnspan=2)
        self.bet1 = tk.Entry(self,width=5, font=betfont)
        self.button_confirm = tk.Button(self, text = "confirm", font = font1, highlightbackground = "tomato", command = self.confirmBet)
        #don't put them on the grid yet

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

        pot_label = tk.Label(self, text = str(newgame.pot), font = font1, fg = "yellow", bg = "black")
        pot_label.grid(column = 3, row = 2, columnspan = 2, sticky = "nsew")
        
        self.boardID1 = self.background.create_image(200,196,image = back)
        self.boardID2 = self.background.create_image(305,196,image = back)
        self.boardID3 = self.background.create_image(410,196,image = back)
        self.boardID4 = self.background.create_image(515,196,image = back)
        self.boardID5 = self.background.create_image(620,196,image = back)


    def confirmBet(self):
        self.bet1.grid_forget()
        self.button_confirm.grid_forget() # hide the buttons
        amount = int(self.bet1.get())
        if amount > 0:
            pot += amount
            #add the cover again
            #minus from player money
        else:
            betLabel = tk.Label(self, text = "Please enter a legal bet", font = font1, fg = "blue", height = 3, width = 20, bg = "black")
            betLabel.grid(column = 8, row = 5, sticky = "nsew")

        
    def betSize(self):
        self.bet1.grid(row = 6, column = 5) # put the button and bet box on the grid
        self.button_confirm.grid(row = 6, column = 6)
        self.bet1.delete(0,"end") # clear box
        self.bet1.focus_set() # move cursor to the box


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