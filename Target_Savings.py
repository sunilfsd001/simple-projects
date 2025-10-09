#Target amount of Savings

def deposite():
 check=input("Do you want to deposite?(y/n)")
 balance=0
 target=int(input("Enter the target amount to start")) 
 if check.upper()=='Y':
    while True:
        print(f"Balance amount to save {target-balance}")
        dep_am=int(input("Enter the deposite amount :"))
        balance+=dep_am
        if balance<target:
            print("You have not reached the target amount.")
            print(f"Your balance is {balance}")
        else:
             print("You have reached the target amount.")
             break
    else: 
        print("Thank you for visiting us...")
 else:
    print("Thank you for visiting us...")

deposite()