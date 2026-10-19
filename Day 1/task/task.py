print("welcome to treasure island.")
print("your mission is to find the treasure.")

choice1 = input('you\'re at a cross road. where do you want to go? type "left" or "right" \n').lower()

if choice1 == "left":
    choice2 = input('you\'ve come to lake. type "wait" to wait for a boat. type "swim to swim cross. \n').lower()
    if choice2 == "wait":
       choice3 = input("there is a house with three doors. red, yellow and blue.which door? \n").lower()

       if choice3 == "red":
           print("room full of fire. game over.")
       elif choice3 == "yellow":
           print("you found the treasure! you win!")
       elif choice3 == "blue":
           print("room of the bests. game over!")
       else:
           print("wrong door. game over")
    else:
       print("attacked by trout. Game over.")
else:
    print("fell into hole. game over. ")