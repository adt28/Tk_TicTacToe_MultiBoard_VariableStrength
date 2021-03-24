"""
TicTacToe On Tkinter - MultiBoard-VariableStrength
Developed By A.D.Tejpal - 24-Mar-2021
=====================================
Human Player Vs Computer - (Human Player Has First Move)

Fill A Row, Column Or Diagonal To Win.

It is a tie if all the slots get filled without any player completing a winning combination.

It is a stalemate (draw), if despite free slots being available, winning combination is no longer feasible.

Board Size Options: 3x3, 4x4, 5x5, 6x6, 7x7 & 8x8

Difficulty Level ( i.e. Computer Strength):
Options: 0 / 1 / 2  (Default Level Is 1)
Level 0 - Computer plays random moves and discontinues blocking opponents victory, after 50% slots get filled up
Level 1 - Computer plays optimum moves but discontinues blocking opponents victory, after 70% slots get filled up
Level 2 - Computer plays at full strength as follows:
     (a) Firstly, go for immediate win if available.
     (b) Otherwise, block opponent if on the verge of immediate win.
     (c) Otherwise, pick up a move from shortest winning path available.

Result (Running Score) can be viewed by clicking 'Score Show/Hide' button

At any stage, fresh game can be started by clicking 'New Game' button

Dictionary design for storing button pointers & relevant values:
btn_dict = {
1:[[b3,3],[b4,4],[b5,5],[b6,6],[b7,7],[b8,8]],
2:[[d0,0],[d1,1],[d2,2]],
3:[[p1,1], [p2,2],----,[p63,63],[p64,64]]}

Dictionary btn_dict holds three lists pertaining to different groups
Key 1 for boardsizebtn_list
Key 2 for levelbtn_list
Key 3 for playbtn_list

In turn, these lists have sublists for individual buttons of that group
Each such sublist has two elements (button object pointer & button value (i.e. position))
"""
import tkinter as tk
import tkinter.messagebox as msgbox
import random

class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TIC TAC TOE: Fill Any Row/Column/Diagonal To Win")

        # Let us adjust tk.Tk window to cover available screen size
        # Argument String for geometry():
        # "width x height + x_offset + y_offset"
        # (Offsets are w.r.t. top left corner of screen)
        self.screen_wd = self.winfo_screenwidth()
        self.screen_ht = self.winfo_screenheight()
        self.geometry("%dx%d+%d+%d" % (
            self.screen_wd, self.screen_ht, 0, 0))

##        # Following style can be used if positioning is not important.
##        self.minsize(screen_wd, screen_ht)
##
##        # For full screen window, following statement can be used:
##        self.attributes('-fullscreen', True)

        self.start_x = 10  # x offset of first widget on top left
        self.start_y = 10  # y offset of first widget on top left

        self.level_list = [0, 1, 2]  # Difficulty Levels
        self.board_list = [3, 4, 5, 6, 7, 8]  # Board Size

        # Some dictionaries, lists etc:
        self.btn_dict = {}  # Dictionary holding lists of buttons
        self.boardsizebtn_list = []  # List for board size buttons
        self.levelbtn_list = []  # List for difficulty level buttons
        self.playbtn_list = []  # List for play buttons
        self.freeslot_list = []  # List for unoccupied slots
        self.wincomb_list = []  # List of possible winning combinations
        self.haswon_list = []  # List of actual winning combination
        self.playermove_list = []  # List for player's moves
        self.compmove_list = []  # List for computer's moves

        # Some other initial values:
        self.cum_x = 0
        self.cum_y = 0
        self.rows = 3  # Default Value
        self.level = 1  # Default Value
        self.fontsize_hdg = int(0.04 * self.screen_ht)
        self.winner = ""  # Winning Player - X or O
        self.stalemate = False
        self.click_disabled = False

        # Some Actions At StartUp
        self.score_dict = self.make_scoredict()
        self.make_widgets()
        self.show_playboard()

    def make_scoredict(self):
        """
        It bulds a dictionary of sub-dictionaries for Running Score:    
        Parent Dictionary Keys (0, 1 2): For Computer Strength Level
        Sub-Dictionary Keys (e.g. 3, 4, 5, 6, 7, 8): For Board Size
        Each sub-dictionary has a sub-list with three elements.
        Elements in each sub-list: PlayerWin, ComputerWin, Drawn
        """
        # Initialize main dictionary serving as overall container
        scdict = {}
        for lev in self.level_list:
            # Initialize Sub-Dictionaries For Each Difficulty Level
            scdict[lev] = {}
            for board in self.board_list:
                # Initialize Sub-Lists For Each Board - For Each Level
                scdict[lev][board] = [0, 0, 0]

        return scdict

    def make_widgets(self):        
        lbwd_hdg = int(0.35 * self.screen_wd)  # Hdg Label Width
        lbht_hdg = int(0.07 * self.screen_ht)  # Hdg Label Height
        lbht_subhdg = int(0.6 * lbht_hdg)  # SubHdg Label Height
        
        # Create a micro-label for displaying running score
        # Place it at top left
        fontsize = int(self.fontsize_hdg / 2)
        self.score_label = tk.Label( self,
            text="", 
            font="Times "+str(fontsize)+" bold",
            bg="white", fg="black",
            bd=5, relief="ridge")
        self.score_label.place(x = 0, y = 0,
            width=1, height=1)
        
        # Heading Label
        # relief argument (other than flat) is needed for border display
        # relief values: flat, raised, sunken, ridge, solid, groove
        # borderwidth & bd can be used interchangeably
        lb = tk.Label(self, text="Tic Tac Toe", 
            font="Times "+str(self.fontsize_hdg)+" bold",
            bg="white", fg="black", bd=4, relief="ridge")
        lb.place(x = self.start_x, y = self.start_y,
            width=lbwd_hdg, height=lbht_hdg)
        self.cum_x = self.cum_x + self.start_x + lbwd_hdg
        self.cum_y = self.cum_y + self.start_y + lbht_hdg
        
        # Label for selecting board size:
        # anchor="w" can be used for left justification of text
        # (Screen left is regarded as west i.e. "w")
        vertgap = 5
        self.cum_y = self.cum_y + vertgap
        fontsize = int(self.fontsize_hdg / 2)
        txt = "Select Board Size"
        lb = tk.Label(self, text=txt,
            font="Times "+str(fontsize)+" bold",
            bg="white", fg="black", bd=2, relief="solid")
        lb.place(x = self.start_x, y = self.cum_y,
            width=lbwd_hdg, height=lbht_subhdg)

        self.cum_y = self.cum_y + lbht_subhdg

        # Buttons for selecting board size (b3 to b8):
        # (i.e. number of rows: 3/4/5/6/7/8):
        for c in range(0, 4, 3):
            for r in range(3, 6):
                # As default, show first button (3x3) in selected state
                if c + r == 3:
                    bwd = 3  # Border Width
                    clr = "light green"
                else:
                    bwd = 1
                    clr = "light gray"

                # A list is passed as argument for btn_click() function
                # First element stands for the btn group, used as key in buttons dictionary btnDict
                # (e.g. 1 for board size, 2 for difficulty level, 3 for play buttons)
                # 2nd element of this list stands for index position of this button's sublist in boardSizeBtnList
                # Each button's sublist has two elements (button object pointer & board size)
                # These sublists get appended to boardsizebtn_list
                # boardsizebtn_list gets stored in dictionary btn_dict
                btnwd = int(lbwd_hdg/3)
                btnht = int(0.7 * lbht_hdg)
                fontsize = int(self.fontsize_hdg / 2)
                btn = tk.Button(self, text=str(c + r) + "x" + str(c + r), 
                    font="Times "+str(fontsize)+" bold",
                    bg=clr, fg="black", bd=bwd,
                    command = lambda z = c+r-3: self.btn_click(list((1,z))))
                btn.place(x = self.start_x + btnwd * (r - 3),
                    y = self.cum_y, width=btnwd, height=btnht)
                btn_sublist = [btn, c+r]
                self.boardsizebtn_list.append(btn_sublist)

            self.btn_dict[1] = self.boardsizebtn_list
            self.cum_y = self.cum_y + btnht

        # Label for selecting Difficulty level (i.e. computer strength):
        # anchor="w" can be used for left justification of text
        # (Screen left is regarded as west i.e. "w")
        txt = "Select Difficulty Level"
        self.cum_y = self.cum_y + vertgap
        fontsize = int(self.fontsize_hdg / 2)
        lb = tk.Label(self, text=txt,
            font="Times "+str(fontsize)+" bold",
            bg="white", fg="black", bd=2, relief="solid")
        lb.place(x = self.start_x, y = self.cum_y,
            width=lbwd_hdg, height=lbht_subhdg)
        self.cum_y = self.cum_y + lbht_subhdg

        # Buttons for selecting difficulty level:
        # (0 for weak, 1 for medium, 2 for full strength):
        for d in range(3):
            btnwd = int(lbwd_hdg/3)
            btnht = int(0.7 * lbht_hdg)
            fontsize = int(self.fontsize_hdg / 2)
            
            # As default, show the button for level 1 in selected state
            if d == 1:
                bwd = 3  # Border Width
                clr = "light green"
            else:
                bwd = 1
                clr = "light gray"

            # A list is passed as argument for btn_click() function
            # First element stands for the btn group, used as key in buttons dictionary btnDict
            # (e.g. 1 for board size, 2 for difficulty level, 3 for play buttons)
            # 2nd element of this list stands for index position of this button's sublist in boardSizeBtnList
            # Each button's sublist has two elements (button object pointer & board size)
            # These sublists get appended to levelbtn_list
            # levelbtn_list gets stored in dictionary btn_dict
            btn = tk.Button(self, text=str(d), 
                font="Times "+str(fontsize)+" bold",
                bg=clr, fg="black", bd=bwd,
                command = lambda z = d: self.btn_click(list((2,z))))
            btn.place(x = self.start_x + btnwd * d,
                y = self.cum_y, width=btnwd, height=btnht)
            btn_sublist = [btn, d]
            self.levelbtn_list.append(btn_sublist)

        self.btn_dict[2] = self.levelbtn_list
        self.cum_y = self.cum_y + btnht

        # Create 64 micro play buttons for Game Board
        # Place these buttons at top left corner of screen
        fontsize = int(self.fontsize_hdg / 2)
        for p in range(1, 65):
            # A list is passed as argument for btn_click() function
            # First element stands for the btn group, used as key in buttons dictionary btnDict
            # (e.g. 1 for board size, 2 for difficulty level, 3 for play buttons)
            # 2nd element of this list stands for index position of this button's sublist in boardSizeBtnList
            # Each button's sublist has two elements (button object pointer & board size)
            # These sublists get appended to playbtn_list
            # playbtn_list gets stored in dictionary btn_dict
            btn = tk.Button(self, text=str(p), 
                font="Times "+str(fontsize)+" bold",
                bg="light gray", fg="black",
                command = lambda z = p - 1: self.btn_click(list((3,z))))
            btn.place(x = 0, y = 0, width=1, height=1)
            btn_sublist = [btn, p]
            self.playbtn_list.append(btn_sublist)

        self.btn_dict[3] = self.playbtn_list

        # Create Mesage Label:
        vertgap = 5
        self.cum_y = self.cum_y + vertgap
        lbht = int(0.85 * (self.screen_ht - self.cum_y)) \
            - int(0.7 * lbht_hdg)  # Allowing space for bottom button
        fontsize = int(self.fontsize_hdg / 2)

        self.notification_label = tk.Label( self,
            text="Notifications", 
            font="Times "+str(fontsize)+" bold",
            bg="white", fg="black",
            bd=5, relief="ridge")
        self.notification_label.place(x = self.start_x, y = self.cum_y,
            width=lbwd_hdg, height=lbht)
        self.cum_y = self.cum_y + lbht
        self.notification_update()

        # Create buttons for New Game & For Running Score:
        vertgap = 5
        self.cum_y = self.cum_y + vertgap
        btnwd = int(lbwd_hdg / 2)
        btnht = int(0.7 * lbht_hdg)
        fontsize = int(self.fontsize_hdg / 2)
        self.newgame_btn = tk.Button(self, text="New Game", 
            font="Times "+str(fontsize)+" bold",
            bg="light gray", fg="black", bd=bwd,
            command = self.show_playboard)
        self.newgame_btn.place(x = self.start_x,
            y = self.cum_y, width=btnwd, height=btnht)

        self.score_btn = tk.Button(self, text="Score Show/Hide", 
            font="Times "+str(fontsize)+" bold",
            bg="light gray", fg="black", bd=bwd,
            command = self.toggle_score)
        self.score_btn.place(x = self.start_x + btnwd,
            y = self.cum_y, width=btnwd, height=btnht)

        self.cum_y = self.cum_y + btnht
        
    def toggle_score(self):
        if len(self.score_label["text"]) > 0:
            self.hide_score()
        else:
            self.show_score()

    def show_score(self):
        txt = self.get_score()
        lbwd = int(0.85 * (self.screen_wd - self.cum_x))
        lbht = self.cum_y - self.start_y
        self.score_label.place(x = self.cum_x + 20,
            y = self.start_y, width=lbwd, height=lbht)
        self.score_label.lift()
        self.score_label["text"] = self.get_score()
        

    def hide_score(self):
        self.score_label["text"] = ""
        self.score_label.place(x = 0,
            y = 0, width=1, height=1)

    def notification_update(self, msg=""):
        txt = ""
        msg1 = "Selected Board: " \
            + str(self.rows) + "x" + str(self.rows)
        msg1 = msg1 + "\nSelected Difficulty Level: " \
            + str(self.level)
        msg1 = msg1 + "\n\nYou Play As X And Move First"
        msg1 = msg1 + "\nComputer Plays As O"
        msg1 = msg1 + "\n\nClick Any Free Button on PlayBoard"
        msg1 = msg1 + "\nTo Win: Fill A Row/Column/Diagonal"
        if len(msg) > 0:
            txt = msg
        else:
            txt = msg1

        self.notification_label["text"] = txt

    def show_playboard(self):
        self.hide_score()
        self.notification_label["bg"] = "white"

        # Reset initial values
        self.winner = ""
        self.stalemate = False
        self.click_disabled = False
        self.haswon_list = []
        self.playermove_list = []
        self.compmove_list = []
        
        # rebuild freeslot_list & wincomb_list
        # (as per latest selected board size)
        # wincomb_list is a list of all possible winning combinations
        self.freeslot_list = [s for s in range(1, 1 + self.rows * self.rows)]
        self.wincomb_list = self.make_wincomblist()
        self.notification_update()
        
        # Reposition play buttons at top left corner of screen
        # (In micro-size)
        for sublist in self.playbtn_list:
            btn = sublist[0]
            btn["text"] = str(sublist[1])
            btn["bg"] = "light gray"
            btn["fg"] = "black"
            fontsize = int(self.fontsize_hdg / 2)
            btn["font"] = "Times "+str(fontsize)+" bold"
            btn.place(x =0, y =0, width=1, height=1)

        board_wd = int(0.85 * (self.screen_wd - self.cum_x))
        board_ht = self.cum_y - self.start_y

        btn_wd = int(board_wd / self.rows)
        btn_ht = int(board_ht / self.rows)
        self.playmark_fontsize = int(0.6 * btn_ht)

        board_x = self.cum_x + 20
        board_y = self.start_y

        # Outer loop defines first column
        # Inner loop for rows starting with each element of this column
        row = 0
        for c in range(1,
            (self.rows * self.rows) - self.rows + 2, self.rows):
            for r in range(0, self.rows):
                btn_sublist = self.playbtn_list[c+r-1]
                btn = btn_sublist[0]
                btn.place(x =board_x + btn_wd * r,
                    y =board_y + btn_ht *  row,
                    width=btn_wd, height=btn_ht)
                
            row  = row + 1

    def make_wincomblist(self):
        """
        Builds a list of sublists of potential Winning Combinations
        (Rows, Columns & diagonals)
        """
        wlist = []
        
        # SubLists for row combinations
        for x in range(1,
            (self.rows * self.rows - (self.rows - 1) + 1), self.rows):
            sublist = []
            for n in range(self.rows):    
                sublist.append(n + x)

            wlist.append(sublist)

        # SubLists for column combinations
        for x in range(1, self.rows + 1):
            sublist = []
            for n in range(x,
                x + (self.rows * self.rows - (self.rows - 1) + 1), self.rows):
                sublist.append(n)

            wlist.append(sublist)

        """
        SubLists of two diagonal-wise combinations
        This loop runs only for two cycles
        In first one, it starts at first slot in top row
        In 2nd round, it starts at last slot in top row
        """
        # Step margin between adjacent values - First Diagonal
        sp = self.rows + 1
        for x in range(1, self.rows + 1, self.rows - 1):
            sublist = []
            ct = 0        
            while ct < self.rows:
                n = x + sp * ct
                sublist.append(n)
                ct = ct + 1

            # Step margin between adjacent values - 2nd Diagonal
            sp = self.rows - 1

            wlist.append(sublist)

        return wlist

    def get_bestmove_list(self, move_list):
        """
        Based upon moves made so far (moveList), it returns shortest list of remaining moves for win.
        
        wincomb_list is a list having sub-lists of possible winning combinations for rows, columns & diagonals
        """
        # Initialize default value of bestmove_list
        bmlist = [*self.freeslot_list]
        # If only one slot is free, no need to check further. 
        if len(bmlist) > 1:
            for x in self.wincomb_list:
                # Intersection of current sublist of winning combinations and moves made so far
                s1 = [item for item in x if item in move_list]

                if len(s1) > 0: 
                    # Intersection difference of current sublist and s1
                    # This represents the balance moves for win
                    s2 = [item for item in x if item not in s1]
                    
                    # Intersection of s2 & free slots
                    # (i.e. whether all potential slots in balance win list are free)
                    s3 = [item for item in s2 if item in self.freeslot_list]

                    # If all slots in s2 are free and s2 is shorter than bmList, assign the contents of s2 to s 
                    if len(s2) == len(s3) and len(s2) < len(bmlist):
                        bmlist = [*s2]

                if len(bmlist) == 1:
                    # This is a winning move. No need to explore further.
                    break

        return bmlist

    def get_wonlist(self, move_list):
        """
        If game won, returns the list of completed row/column/diagonal
        Otherwise, an empty list
        wincomb_list: A list having sub-lists of possible winning combinations of rows, columns & diagonals
        """
        wlist = []
        moveset = set(move_list)
        for x in self.wincomb_list:
            if set(x).issubset(moveset):
                wlist = x
                break

        return wlist

    def haswon(self, move_list):
        """
        Finds whether move_list represents Victory
        (completed row/column/diagonal)

        wincomb_list: A list having sub-lists of possible winning combinations for rows, columns & diagonals
        """
        won = False
        moveset = set(move_list)
        for x in self.wincomb_list:
            if set(x).issubset(moveset):
                won = True
                break

        return won

    def is_stalemate(self):
        """
        Finds whether whether the game has reached a stalemate
        (Despite free slots, winning combination is no longer feasible)

        wincomb_list: A list of sub-lists of possible winning combinations for rows, columns & diagonals
        """
        smate = True
        for x in self.wincomb_list:
            # Check if any sublist of winning combinations is still pure
            # (Free from a mix of player & computer moves in same sublist)
            if len([item for item in x if item in self.playermove_list]) == 0 \
                or len([item for item in x if item in self.compmove_list]) == 0:
                smate = False
                break

        return smate

    def get_compmove(self):
        """
        Determines computer's next move.
        wincomb_list: A list having sub-lists of winning combinations for rows, columns & diagonals
        compmove_list is a list holding moves made by the computer.
        playermove_list is a list holding moves made by the player.
        freeslot_list is a list of free slots still available.

        level is the difficulty level, i.e. strength setting for computer
        Options: 0 / 1 / 2  (Defaul Level Is 1)
        Level 0 - Computer plays random moves and discontinues blocking opponents victory, after 50% slots get filled up
        Level 1 - Computer plays optimum moves but discontinues blocking opponents victory, after 70% slots get filled up
        Level 2 - Computer plays at full strength as follows:
             (a) Firstly, go for immediate win if available.
             (b) Otherwise, block opponent if on the verge of immediate win.
             (c) Otherwise, pick up a move from shortest winning path available.
        """
        if len(self.freeslot_list) == 0:
            # No move available
            return 0
        
        cm = 0  # default value for computer move
        
        # Get the list of best moves available for player
        bestplayermove_list = self.get_bestmove_list(
            self.playermove_list)
        
        if self.level > 0:
            # Get the list of best moves available for computer
            bestcompmove_list = self.get_bestmove_list(
                self.compmove_list)
            
            if len(bestcompmove_list) > 1:
                # There is no immediate win for computer.
                # Check if the player has an immediate win in sight
                if len(bestplayermove_list) == 1:
                    # There is an immediate win for player.
                    # Block it if level is 2
                    # Or for level 1 and more than 30% free slots available
                    if self.level ==2 or (self.level == 1 and
                        len(self.freeslot_list) > \
                            round((self.rows * self.rows * 0.3))):
                        # Block opponent's win
                        cm = bestplayermove_list[0]
                else:
                    # Select a random value from bestcompmove_list
                    cm = random.choice(bestcompmove_list)
            else:
                # The computer has an immediate winning move:
                cm = bestcompmove_list[0]
        else:
            # Computer is playing at level 0 (weak strength)
            # If more than 50% free slots are still available
            # And the player has an immediate win in sight, block it
            if len(bestplayermove_list) == 1 and \
                len(self.freeslot_list) > \
                round((self.rows * self.rows * 0.5)):
                    cm = bestplayermove_list[0]

        if cm == 0:
            # Select a random value from freeslot_list
            cm = random.choice(self.freeslot_list)

        return cm

    def update_scoredict(self, 
        playerwin, compwin, drawn):
        # The arguments: 0 or 1 (e.g. 1,0,0 / 0,1,0 / 0,0,1)
        self.score_dict[self.level][self.rows][0] = \
            self.score_dict[self.level][self.rows][0] + playerwin
        self.score_dict[self.level][self.rows][1] = \
            self.score_dict[self.level][self.rows][1] + compwin
        self.score_dict[self.level][self.rows][2] = \
            self.score_dict[self.level][self.rows][2] + drawn

    def get_score(self):
        txt = ""
        totgames = 0
        totplayerwins = 0
        totcompwins = 0
        totdrawn = 0
        for lev in self.level_list:
            subdict = self.score_dict[lev]
            for board in self.board_list:
                scorelist = subdict[board]
                games = sum(scorelist)
                totgames = totgames + games
                totplayerwins = totplayerwins + scorelist[0]
                totcompwins = totcompwins + scorelist[1]
                totdrawn = totdrawn + scorelist[2]
                if games > 0:
                    txt = txt + "\nDifficulty Level: " + str(lev) \
                        + ", Board Size: " + str(board) + "x" + str(board)
                    txt= txt + "\nGames: " \
                         + str(games) + ", PlayerWins: " \
                        + str(scorelist[0]) + ", CompWins: " \
                        + str(scorelist[1]) + ", Drawn: " \
                        + str(scorelist[2]) + "\n"

        #txt = txt + "\nOverAll Summary-Grand Total:"
        txt1 = "\nOverAll Summary-Grand Total:"
        txt1 = txt1 + "\nTot Games: " \
            + str(totgames) + ", PlayerWins: " \
            + str(totplayerwins) + ", CompWins: " \
            + str(totcompwins) + ", Drawn: " + str(totdrawn)
        txt = "Cumulative Score:" + txt1 + "\n" + txt
        return txt

    def blink(self, blinkobject, cycles=6, delay=200):        
        self.ct = 0    
        # Store initial colors
        bc = blinkobject.cget("background")
        fc = blinkobject.cget("foreground")
        
        self.blink_blinker(blinkobject, bc, fc, cycles, delay)

    def blink_blinker(self, blinkobject, bc, fc, cycles, delay):
        if self.ct < cycles:
            self.ct = self.ct + 1
            b = blinkobject.cget("background")
            f = blinkobject.cget("foreground")
            blinkobject.configure(background=f, foreground=b)

            # Make recursive call to this very function (blink_blinker)
            # Imp: Omit function's parenthesis. Pass arguments using coma
            self.after(delay, self.blink_blinker,
                blinkobject, bc, fc, cycles, delay)
        else:
            blinkobject.configure(
                background=bc,
                foreground=fc)

    def btn_click(self, keylist):
        # self.click_disabled takes care of unwanted double clicks
        if self.click_disabled:
            return

        self.click_disabled = True
        btnlistkey = keylist[0]
        btnlist = self.btn_dict[btnlistkey]
        btnsublist_index = keylist[1]
        btnsublist = btnlist[btnsublist_index]
        btn = btnsublist[0]
        btnval = btnsublist[1]
        
        if btnlistkey < 3:
            if len(self.freeslot_list) < self.rows * self.rows:
                msgbox.showinfo("Game In Progress",
                    "These Settings Can't Be Disturbed\n" \
                    + "As Game Is In Progress\n" \
                    + "Click The 'New Game' Btn For Fresh Start")
            else:            
                # These buttons pertain to board size
                # or difficulty selection
                # At first, normalize their appearance
                for btnsublist in btnlist:
                    b = btnsublist[0]
                    b.config(bg="light gray", bd = 1)

                # Highlight the clicked button in green
                btn.config(bg="light green", bd = 3)
                if btnlistkey == 1:
                    self.rows = btnval
                else:
                    self.level = btnval

                self.show_playboard()

        else:
            if len(self.winner) > 0 or self.stalemate \
                or len(self.freeslot_list) == 0:
                return   # Game Finished
                
            if btnval in self.freeslot_list:
                btn["text"] = "X"
                btn["bg"] = "blue"
                btn["font"] = "Times " \
                    +str(self.playmark_fontsize)+" bold"
                btn["fg"] = "white"
                self.game_on = True

                # Update the status of freeslot_list
                self.freeslot_list = list(
                filter(lambda x: x != btnval, self.freeslot_list))

                self.playermove_list.append(btnval)
                
                self.haswon_list = \
                    self.get_wonlist(self.playermove_list)
                if len(self.haswon_list) > 0:
                    self.winner = "X"

                if not self.stalemate and self.winner == "" \
                    and len(self.freeslot_list) > 0:
                    # Get Computer's Move
                    move = self.get_compmove()
                    if move > 0:
                        btnsublist = self.playbtn_list[move - 1]
                        btn = btnsublist[0]
                        btn["text"] = "O"
                        btn["bg"] = "purple"
                        btn["font"] = "Times " \
                            +str(self.playmark_fontsize)+" bold"
                        btn["fg"] = "white"
                        self.blink(btn)

                        # Update the status of freeslot_list
                        self.freeslot_list = list(
                            filter(lambda x: x != move, self.freeslot_list))
                        
                        self.compmove_list.append(move)
                        
                        self.haswon_list = \
                            self.get_wonlist(self.compmove_list)
                        if len(self.haswon_list) > 0:
                            self.winner = "O"

            self.game_status()
                
        self.click_disabled = False


    def game_status(self):
        if len(self.winner) > 0:
            if self.winner == "X":
                self.update_scoredict(1, 0, 0)
                txt = "Congratulations!\nYou (X)  have Won!"  \
                    + "\n\nWinning Set Is: \n" + str(self.haswon_list)
                
                msgbox.showinfo("Well Done!", 
                    "Congratulations!  You (X)  have Won!"  \
                    "\nWinning Set Is: " + str(self.haswon_list))
            else:
                self.update_scoredict(0, 1, 0)
                txt = "Computer (O) Has Won!"  \
                    + "\nBetter Luck Next Time!" \
                    + "\n\nWinning Set Is: \n" + str(self.haswon_list)
                
                msgbox.showinfo("Computer Has Won!",
                    "Better Luck Next Time! Computer (O)  has Won!"  \
                    "\nWinning Set Is: " + str(self.haswon_list))
        else:
            self.stalemate = self.is_stalemate()
            if self.stalemate or len(self.freeslot_list) == 0:
                self.update_scoredict(0, 0, 1)                
                if self.stalemate:
                    txt = "IT IS A STALEMATE" \
                        + "\nGame Is Dead & Drawn."
                        
                    msgbox.showinfo("STALEMATE",
                        "StaleMate! Game Is Dead & Drawn.")
                else:
                    txt = "GAME DRAWN" \
                        + "\nIt Is A Tie! No Winner"
                    
                    msgbox.showinfo("Game Drawn",
                        "It Is A Tie! Game Drawn.")

        if len(self.winner) > 0 or \
            self.stalemate or len(self.freeslot_list) == 0:
            txt1 = "\n\nFor Score: " \
                + "\nClick 'Score Show/Hide' Btn" \
                + "\n\nFor New Game: " \
                + "\nClick 'New Game' Button"
            self.notification_label["text"] = txt + txt1
            self.notification_label["bg"] = "yellow"

#============================

if __name__ == "__main__":
    ttt = TicTacToe()
    ttt.mainloop()
    
