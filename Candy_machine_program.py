# candy machine program

def candies(quantity):  #function
    available_candies=10000  
    price=1.5
    print(f"The amount to be paid is {quantity * price}")
    paid=input("Amount paid ? (y/n)")
    while True:
        if paid.lower()=='y':
            if quantity<=available_candies:
                print("Dropping candies.......")
                available_candies-=quantity    # subtracting the candies after dropping from the machine 
                print("Plss take your candies from the machine")
                print(f"Now available candies quantity is {available_candies}") # Printing available candies after dropping
                break
            else:
                print("Sorry! we dont have that much of candies pls try with different quantity")
        else:
            print("Please pay the amount for candies")

# Main code

to_continue=input("Do you want candies?(y/n)\n") # Asking the user to continue or not 
if to_continue.upper()=='Y':
    quantity=int(input("How many candies do you want ?"))    # asking the user to enter the quantity of candies they want 
    candies(quantity)   # calling the function and passing the quantity of candies
elif to_continue.upper()=='N':
    print("Thank you for visiting us")
else:
    print("Enter a valid input")