# Tk_TicTacToe_MultiBoard_VariableStrength 

Developed By A.D.Tejpal - 24-Mar-2021
==========================================
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
