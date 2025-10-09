# User authentication 

def auth():
    password="python123"
    attempt=3   # attempts
    login=input("Do you want to login?(y/n)")
    while login.upper()=='Y':
        passcode=input("Enter the password :")
        if passcode==password and attempt>=0:  # Checking the password and attempts
            print("You logged in successfully....")
            break
        elif attempt!=1:
            print("Enter the correct password...")
            attempt-=1
        else:
            print("Failed to login")
            break
    else:
        print('You entered a wrong input')
auth()