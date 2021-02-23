#games/DiceRolling/pysrc/main.py
#python 3.8.2, replit. 
#Jefaxe
#miniProjects
#imports
import random
dicePlayer1=[]
dicePlayer2=[]

#aim is to hit exactly 21
#this will be in REAME.md on github
Player1_name = input("PLAYER 1: What is your name?")
Player2_name = input("PLAYER 2: What is your name?")
no_of_rolls = int(input("MASTER: How many rolls should there be per player?"))
#defines the dice array
for i in range(0,no_of_rolls):
    dicePlayer1.append(None)
    dicePlayer2.append(None)
for i in range(no_of_rolls):
    #ask for player 1
    print(Player1_name,": Press ENTER to roll, or type SKIP to skip the roll and keep your current score")
    decision = input().upper
    if decision == "SKIP":
        print("Skipping dice rolling..")
    else:
        dicePlayer1[i] = random.randint(0,6)
    print(Player1_name,": rolled",dicePlayer1[i])
    #ask for player 2
    print(Player2_name,": Press ENTER to roll, or type SKIP to skip this roll and keep your current score")
    decsion = input()
    if decision == "SKIP":
        print("Skipping dice rolling..")
    else:
        dicePlayer2[i] = random.randint(0,6)
    print(Player2_name,": rolled",dicePlayer2[i])

Player1_total = 0
Player2_total = 0
for i in dicePlayer1:
    Player1_total+=i
    #this adds up all of the player's scores.
for i in dicePlayer2:
    Player2_total+=i

if abs(Player1_total-21)<abs(Player2_total-21):
    print(Player2_name,": wins with a score of", Player2_total)

elif abs(Player2_total-21)<abs(Player1_total-21):
    print(Player1_name,": wins with a score of", Player1_total)



