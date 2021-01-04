import tkinter as tk
from collections import defaultdict
import random

class tiktok2():
    def __init__(self):
        self.root=tk.Tk()
        self.borde_list=[[0,0,0],[0,0,0],[0,0,0]]
        self.symbol={0:'',1:'X',-1:'O'}
        self.player=1
        self.alpha=0.5
        self.discount=0.5
        self.q_table=defaultdict(lambda:defaultdict(lambda:0.0))
            
    def update(self, state, action, new_state, reward):
        value=self.q_table[state][action]
        v=list(self.q_table[new_state].values())
        if not v:
            v=0
        new_state_max=max(v)
        value=value+self.alpha*(reward+self.discount*new_state_max-value)
        self.q_table[state][action]=value
        
    def get_best_action(self,state):
        keys = list(self.q_table[state].keys())
        if not keys:
            return None
        return max(keys, key=lambda x: self.q_table[state][x])
##        value=list(self.q_table[new_state])
##        print("value",value)
##        if not value:
##            return None
##        for key, values1 in self.q_table[new_state].items():
##            if values1==max(value):
##                print(key)
##                return key
    def get_action(self,new_state,all_action):
        best=self.get_best_action(str(new_state))
        
        if not best:
            print("random")
            return random.choice(all_action)
        print('best',best)
        return best
        
    def tik_tok2_learn(self):
        step=100
        for i in range(step):
            if i%100==0:
                print(i*100/step,'%')
            while 1:
                state=self.borde_list
                action=self.get_action(state,self.get_valid_action())
                print(action)
                win=self.play(action[0],action[1],False)

                if win != '' or len(self.get_valid_action())==0:
                    self.update(str(state),str(action),str(self.borde_list),100)
                    break
                ##state2=self.borde_list
                ##action2=self.get_action(state2,self.get_valid_action())
                action2=random.choice(self.get_valid_action())
                win=self.play(action2[0],action2[1],False)
                if win!='' or len(self.get_valid_action())==0:
                    self.update(str(state),str(action),str(self.borde_list),-100)
                    break
                self.update(str(state),str(action),str(self.borde_list),0)
            self.try_again(render=False)
    
    def agent_play(self):
       pass 
    def play(self,i,j,render):
        if self.borde_list[i][j]==0:
            self.borde_list[i][j]=self.player
            self.player=self.player*-1
            win=self.winner()
            
            if render == True:
                print("win",win)
                if win != '':
                    self.try_again(render=True)
                state=self.borde_list
                action=self.get_action(state,self.get_valid_action())
                
                self.borde_list[action[0]][action[1]]=self.player
                self.player=self.player*-1
                win=self.winner()
                print("win",win)
                if win != '':
                    self.update(str(state),str(action),str(self.borde_list),100)
                    self.try_again(render=True)
                self.borde_made()
            return win
        
    def get_valid_action(self):
        action_list=[]
        for i in range(3):
            for j in range(3):
                if self.borde_list[i][j]==0:
                    action_list.append((i,j))
        return action_list
    def winner(self):
        for i in range(3):
            row=0
            for j in range(3):
                row=row+self.borde_list[i][j]
                if row==3:
                    return 'X'
                elif row==-3:
                    return 'O'
        for i in range(3):
            row=0
            for j in range(3):
                row=row+self.borde_list[j][i]
                if row==3:
                    return 'X'
                elif row==-3:
                    return 'O'
        if (self.borde_list[0][0]== 1 and self.borde_list[1][1] == 1 and self.borde_list[2][2]== 1) or (self.borde_list[0][2]== 1 and self.borde_list[1][1] == 1 and self.borde_list[2][0]== 1):
            return 'X'
        if (self.borde_list[0][0]== -1 and self.borde_list[1][1] == -1 and self.borde_list[2][2]== -1) or (self.borde_list[0][2]== -1 and self.borde_list[1][1] == -1 and self.borde_list[2][0]== -1):
            return 'O'
        return '';
    def borde_made(self):
        tk.Button(self.root,text=self.dif(0,0),command=lambda:self.play(0,0,True),height=1,width=10).grid(row=0,column=0)
        tk.Button(self.root,text=self.dif(0,1),command=lambda:self.play(0,1,True),height=1,width=10).grid(row=0,column=1)
        tk.Button(self.root,text=self.dif(0,2),command=lambda:self.play(0,2,True),height=1,width=10).grid(row=0,column=2)
        tk.Button(self.root,text=self.dif(1,0),command=lambda:self.play(1,0,True),height=1,width=10).grid(row=1,column=0)
        tk.Button(self.root,text=self.dif(1,1),command=lambda:self.play(1,1,True),height=1,width=10).grid(row=1,column=1)
        tk.Button(self.root,text=self.dif(1,2),command=lambda:self.play(1,2,True),height=1,width=10).grid(row=1,column=2)
        tk.Button(self.root,text=self.dif(2,0),command=lambda:self.play(2,0,True),height=1,width=10).grid(row=2,column=0)
        tk.Button(self.root,text=self.dif(2,1),command=lambda:self.play(2,1,True),height=1,width=10).grid(row=2,column=1)
        tk.Button(self.root,text=self.dif(2,2),command=lambda:self.play(2,2,True),height=1,width=10).grid(row=2,column=2)
        tk.Button(self.root,text='Try Again',command=lambda:self.try_again(render=True),height=1,width=10).grid(row=3,column=0)
        tk.Button(self.root,text='Exit',command=lambda:self.exit(),height=1,width=10).grid(row=3,column=1)
        tk.Button(self.root,text=self.who_play(),height=1,width=10).grid(row=3,column=2)
        
    def main_loop(self):
        self.root.mainloop()
    def who_play(self):
        return self.symbol[self.player]
    def exit(self):
        print("destroy")
        self.root.destroy()
    def try_again(self,render):
        self.borde_list=[[0,0,0],[0,0,0],[0,0,0]]
        self.player=1
        if render==True:
            self.player=-1
            self.borde_made()
    def dif(self,i,j):
        v=self.borde_list[i][j]
        return self.symbol[v]
    
tiktok=tiktok2()
tiktok.borde_made()
print("learning")
tiktok.tik_tok2_learn()
print("learning \n done")
print('let`s play')


tiktok.main_loop()
