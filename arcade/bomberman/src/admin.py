import os
import random
import sys

sys.path.append(os.path.split(sys.path[0])[0])


# client = TCPClient()
# client.connect("localhost",6317)
# client.connect("67.23.28.146", 6317)


def main():
    # client.send_data(["update",None])
    print("1) Clear Data")
    print("2) Reset Users")
    print("3) Add User")
    print("8) Start Game")
    print("9) Exit")

    inp = 0
    while inp != "4":
        inp = input("$: ")

        if inp == "1":
            client.send_data(["update", "clear all"])
        elif inp == "2":
            client.send_data(["update", "reset ids"])
        elif inp == "3":
            client.send_data(["update", "user joined", random.randint(0, 10000000)])
        elif inp == "8":
            client.send_data(["update", "start game"])
        elif inp == "9":
            sys.exit()


if __name__ == "__main__":
    main()
