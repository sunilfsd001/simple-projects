#  Number guess game 

import random as r

game=input("Do you want to play a game?(y/n)\n") # asking the user to play or not 
point=0
level=int(input("Enter the difficult level\n1 - 2 digit\n2 - 3 digit\n3 - 4 digit\n")) # asking user to select the level 
while game.lower()=='y': # Enter while y is a input
  if level==1:
    num=r.randint(1,100) # 2 digit random numbers
  elif level==2:
    num=r.randint(100,1000) # 3 digit random numbers
  elif level==2:
    num=r.randint(1000,10000) # 4 digit random numbers
  else:
    print("Enter the valid input") 
  while True:
      guess=int(input("Enter the number you guessed\n")) # getting input from the user
      if num==guess: # checking the input
        print("You guessed a correct number")
        point+=1
        print(f"Your point is {point}")
        break
      elif num<guess:
        print("Smaller")
      else:
        print("Larger")   
else:
     print("Thank you for your intrest..")