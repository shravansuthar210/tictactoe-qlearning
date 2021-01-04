import tkinter as tk
from tkinter import messagebox
import random
from collections import defaultdict

class tiktok21():
    def __init__(self):
        self.root=tk.Tk()
        self.board_list=[[0,0,0],[0,0,0],[0,0,0]]
        self.symbol={0:'',1:'X',-1:'O'}
        self.player=1
        self.alpha=0.5
        self.discount=0.5
        self.eps = 1.0
        self.q_table=defaultdict(lambda:defaultdict(lambda:0.0))
    def board_made(self):
        tk.Button(self.root,text=self.dif(0,0),command=lambda:self.play(0,0,True,True),height=1,width=10).grid(row=0,column=0)
        tk.Button(self.root,text=self.dif(0,1),command=lambda:self.play(0,1,True,True),height=1,width=10).grid(row=0,column=1)
        tk.Button(self.root,text=self.dif(0,2),command=lambda:self.play(0,2,True,True),height=1,width=10).grid(row=0,column=2)
        tk.Button(self.root,text=self.dif(1,0),command=lambda:self.play(1,0,True,True),height=1,width=10).grid(row=1,column=0)
        tk.Button(self.root,text=self.dif(1,1),command=lambda:self.play(1,1,True,True),height=1,width=10).grid(row=1,column=1)
        tk.Button(self.root,text=self.dif(1,2),command=lambda:self.play(1,2,True,True),height=1,width=10).grid(row=1,column=2)
        tk.Button(self.root,text=self.dif(2,0),command=lambda:self.play(2,0,True,True),height=1,width=10).grid(row=2,column=0)
        tk.Button(self.root,text=self.dif(2,1),command=lambda:self.play(2,1,True,True),height=1,width=10).grid(row=2,column=1)
        tk.Button(self.root,text=self.dif(2,2),command=lambda:self.play(2,2,True,True),height=1,width=10).grid(row=2,column=2)
        tk.Button(self.root,text='Try Again',command=lambda:self.try_again(render=True),height=1,width=10).grid(row=3,column=0)
        tk.Button(self.root,text='Exit',command=lambda:self.exit(),height=1,width=10).grid(row=3,column=1)
        tk.Button(self.root,text=self.who_play(),height=1,width=10).grid(row=3,column=2)
    def set_me_first(self,player):
        self.player=player
    def try_again(self,render):
        self.board_list=[[0,0,0],[0,0,0],[0,0,0]]
        self.player=1
        if render==True:
            self.board_made()
            self.play_Agent()
    
    def main_loop(self):
        self.root.mainloop()
    def who_play(self):
        return self.symbol[self.player]
    def exit(self):
        print("destroy")
        self.root.destroy()
    def dif(self,i,j):
        return self.symbol[self.board_list[i][j]]
    def get_state(self):
        return str(self.board_list)
    def winner(self):
        for i in range(3):
            row=0
            for j in range(3):
                row=row+self.board_list[i][j]
                if row==3:
                    return 'X'
                elif row==-3:
                    return 'O'
        for i in range(3):
            row=0
            for j in range(3):
                row=row+self.board_list[j][i]
                if row==3:
                    return 'X'
                elif row==-3:
                    return 'O'
        if (self.board_list[0][0]== 1 and self.board_list[1][1] == 1 and self.board_list[2][2]== 1) or (self.board_list[0][2]== 1 and self.board_list[1][1] == 1 and self.board_list[2][0]== 1):
            return 'X'
        if (self.board_list[0][0]== -1 and self.board_list[1][1] == -1 and self.board_list[2][2]== -1) or (self.board_list[0][2]== -1 and self.board_list[1][1] == -1 and self.board_list[2][0]== -1):
            return 'O'
        return '';
    def all_valid_action(self):
        action=[]
        for i in range(3):
            for j in range(3):
                if self.board_list[i][j]==0:
                    action.append((i,j))
        return action
    def play(self,i,j,render,me):
        if self.board_list[i][j]==0:
            self.board_list[i][j]=self.player
            self.player=self.player*-1
            win=self.winner()
            if render==True:
                self.board_made()
            if me==True:
                if win!='':
                    messagebox.showinfo(title="always win",message="mere se hoga")
                    self.try_again(True)
                elif len(self.all_valid_action())==0:
                    messagebox.showinfo(title="",message="")
                    self.try_again(True)
                self.play_Agent()
            return win
    def update_q_table(self,state,action,next_state,reward):
        value=self.q_table[state][action]
        v=list(self.q_table[next_state].values())
        next_value=max(v) if v else 0
        value=value+self.alpha*(reward+self.discount*next_value-value)
        self.q_table[state][action]=value
    def get_q_table_action(self,state):
##        row=self.q_table[state]
##        if not row:
##            row=0
##        max_value=max(row)
##        return max_value
        keys = list(self.q_table[state].keys())
        if not keys:
            return None
        return max(keys, key=lambda x: self.q_table[state][x])
    def get_action(self,state,valid_actions):
        if random.random() < self.eps:
            return random.choice(valid_actions)
        action=self.get_q_table_action(state)
        if not action:
            return random.choice(valid_actions)
        return action
    def learn_game(self,n):
        for i in range (n+1):
            if i%10==0:
                print(i*100/n,'%')
            while True:
                state=self.get_state()
                action=self.get_action(state,self.all_valid_action())
                win=self.play(*action,False,False)
                if win!='' or len(self.all_valid_action())==0:
                    self.update_q_table(state,action,self.get_state(),100)
                    break
                win=self.play(*random.choice(self.all_valid_action()),False,False)
                if win != '' or len(self.all_valid_action())==0:
                    self.update_q_table(state,action,self.get_state(),-100)
                    break
                self.update_q_table(state,action,self.get_state(),0)
            self.try_again(False)
            self.eps -= 0.0001
    def play_Agent(self):
        state=self.get_state()
        action=self.get_action(state,self.all_valid_action())
        print(*action)
        win=self.play(*action,True,False)
        if win!='':
            #self.update_q_table(state,action,self.get_state(),100)
            messagebox.showinfo(title="You loss",message="tum se nahi ho payga")
            self.try_again(True)
        elif len(self.all_valid_action())==0:
            messagebox.showinfo(title="",message="")
            self.try_again(True)
##        else:
##            self.update_q_table(state,action,self.get_state(),0)
##        
            
tiktok=tiktok21()
tiktok.learn_game(10000)
tiktok.board_made()

tiktok.play_Agent()
tiktok.main_loop()

