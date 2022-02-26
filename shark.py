import time
import random
fishing = True
a = b = c = d = e = 0 
print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print ("Welcome to Lake Tocowaga")
print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
time.sleep(1)
name = input("What is your name fisherman?")
answer = input("Would you like to go fishing, " + name + "?")
if answer.lower() == "no":
    fishing == False
while fishing == True:    
    time.sleep(1)
    answer = input("Throw out your line, or go home?")
    if answer == "go home":
        fishing = False
        er = float(e / (a + b + c + d))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Thanks for playing " + name + "!")
        print("You caught:", str(a), "cod, ", str(b), "salmon, ", str(c), "shark, ", str(d), "wildfish. \nEfficiency Rate: ", str(er), ".")
    else:
        t = random.randrange(1, 7)
        if t == 1:
            a += 1
            print("You caught a cod!")
        elif t == 2:
            b += 1
            print("You caught a salmon!")
        elif t == 3:
            c += 1
            print("You caught a shark!")
        elif t == 4:
            d += 1
            print("You caught a wildfish!")
        elif t >= 5:
            e += 1
            print("You caught nothing!")
