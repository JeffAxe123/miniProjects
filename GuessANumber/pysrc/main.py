#GuessANumber\pysrc\main.py
#python 3
#import modules
import random

#functions
def is_it_an_integer():
    UserIsStupid = True
    while UserIsStupid:
        try: #attemps to execute the task
            return int(input())
            UserIsStupid = False
        except ValueError: #this code is executed IF ValueError is raised
            print("PROMPT: Please enter a valid integer")
##debug message
#sets the number of chances
print("Please input however many lives you wish to have for this turn.")
NumberOfLives = is_it_an_integer():
print("PRE_LAUNCH: This is a game where you choose a number to guess what the computer has guessed.")
print("PRE_LAUNCH: You have",NumberOfLives,"lives untill you loose.")
#ask the user to input the range of numbers
print("Please enter a rang of values")
#remember that the user may be stupid
RangeOfValues = is_it_an_integer():
#generate the computer's random number
ComputerNumber = random.randint(1,RangeOfValues)
AnswerIsCorrect = False
IsDead = False
while not AnswerIsCorrect and not IsDead:
    print("You have",NumberOfLives,"lives left")
    #ask user for a nummber
    print("Please enter a number between 1 and",NumberOfLives)
    #remember that the user may be stupid
    UserNumber = IsItAnInteger()
    if ComputerNumber == UserNumber:
        print("Your number is perfect")
        AnswerIsCorrect = True
    else:
        if UserNumber > RangeOfValues or UserNumber <=0:
            print("PROMPT: Please input a valid integer between 1 and",RangeOfValues)
        if ComputerNumber > UserNumber:
            print("Your number is too low")
        elif ComputerNumber < UserNumber:
            print("Your number is too high")
        else:
            print("...You have somehow broken maths") # this should never happen
        NumberOfLives-=1
    if NumberOfLives<=0:
        IsDead=True

#end message for success
if not IsDead:
    print("POST_PLAY: You win! :)")
#end message for failure
elif IsDead:
    print("POST_PLAY: You loose :(")
