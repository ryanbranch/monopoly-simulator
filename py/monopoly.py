#File paths
BOARD_FILE = "board.txt"
COMMUNITYCHEST_FILE = "communitychest.txt"
CHANCE_FILE = "chance.txt"

#Card represents a card which is drawn upon landing on a CommunityChest or Chance space
class Space:
    def __init__(self, location_, name_):
        self.location = location_
        self.name = name_

#Space represents any space on the board where a player can land
class Space:
    def __init__(self, location_, name_):
        self.location = location_
        self.name = name_

#Go represents the specific Space on which players begin
#Each time this Space is passed, the passing Player receives passReward
class Go(Space):
    def __init__(self, location_, name_, passReward_):
        Space.__init__(self, location_, name_)
        self.passReward = passReward_

#Property represents a Space which can be owned, on which houses/hotels can be built
#For a property, the self.prices list is of length 3, and has the following meaning:
#   [0]: Printed price (the fee paid by a player to purchase the Space)
#   [1]: Mortgage value (the money received by a player upon selling the Space to the Bank)
#   [2]: Building costs (the cost to add a house to the Space, or to purchase a hotel after 4 houses are owned)
#For a property, the self.rents list is of length 7, and has the following meaning:
#   [0]: Rent (the price paid when a non-owning Player lands on the space, when it is not monopolized)
#   [1]: Monopoly rent (when it is monopolized)
#   [2]: Rent with 1 house
#   [3]: Rent with 2 houses
#   [4]: Rent with 3 houses
#   [5]: Rent with 4 houses
#   [6]: Rent with 1 hotel
class Property(Space):
    def __init__(self, location_, name_, prices_, rents_, color_):
        Space.__init__(self, location_, name_)
        self.prices = prices_
        self.rents = rents_
        self.color = color_

#CommunityChest represents a Space which, when landed on, causes a Player to receive 1 Community Chest card from the corresponding deck
class CommunityChest(Space):
    def __init__(self, location_, name_):
        Space.__init__(self, location_, name_)

#Tax represents a Space which, when landed on, obligates a Player to pay a flat fee or, in some cases, a percentage of their assets to the Bank
#When only a flat fee is allowed, self.percentFee has a value of 0
class Tax(Space):
    def __init__(self, location_, name_, flatFee_, percentFee_):
        Space.__init__(self, location_, name_)
        self.flatFee = flatFee_
        self.percentFee = percentFee_

#Railroad represents a Space which can be owned, and which is part of the railroad network
#For a railroad, the self.prices list is of length 2, and has the following meaning:
#   [0]: Printed price
#   [1]: Mortgage value
#For a railroad, the self.rents list is of length 4, and has the following meaning:
#   [0]: Rent 1 (the price paid when a non-owning Player lands on the space, when the owner owns 1 railroad total)
#   [1]: Rent 2 (when the owner owns 2 railroads total)
#   [2]: Rent 3 (when the owner owns 3 railroads total)
#   [3]: Rent 4 (when the owner owns 4 railroads total)
class Railroad(Space):
    def __init__(self, location_, name_, prices_, rents_):
        Space.__init__(self, location_, name_)
        self.prices = prices_
        self.rents = rents_

#Chance represents a Space which, when landed on, causes a Player to receive 1 Chance card from the corresponding deck
class Chance(Space):
    def __init__(self, location_, name_):
        Space.__init__(self, location_, name_)

#The jail Space. When located on this space, a player can be either "In Jail" or "Just Visiting"
class Jail(Space):
    def __init__(self, location_, name_, maxTurns_, fine_):
        Space.__init__(self, location_, name_)
        self.maxTurns = maxTurns_
        self.fine = fine_

#Utility represents a space which can be owned, where rent is determined by a dice roll multiplier
#For a utility, the self.prices list is of length 2, and has the following meaning:
#   [0]: Printed price
#   [1]: Mortgage value
#For a railroad, the self.rents list is of length 2, and has the following meaning:
#   [0]: Rent 1 (the multiplier when a non-owning Player lands on the space, when the owner owns 1 utility total)
#   [1]: Rent 2 (when the owner owns 2 utilities total)
class Utility(Space):
    def __init__(self, location_, name_, prices_, rents_):
        Space.__init__(self, location_, name_)
        self.prices = prices_
        self.rents = rents_

#FreeParking represents a space which cannot be owned, and which does not cause any action upon landing
class FreeParking(Space):
    def __init__(self, location_, name_):
        Space.__init__(self, location_, name_)

#FreeParking represents a space which cannot be owned, and which sends one who lands upon it to Jail immediately
class GoToJail(Space):
    def __init__(self, location_, name_):
        Space.__init__(self, location_, name_)

class Board:

    def __init__(self):
        self.spaces = []

        with open(BOARD_FILE, 'r') as boardFile:
            for spaceNum, line in enumerate(boardFile):
                lineData = line.split()

                #Builds self.spaces conditionally based on the value of lineData[1]
                idChar = lineData[1]

                #Creates the space newSpace based on lineData and adds it to self.spaces
                #Go Space
                if idChar == 'G':
                    newSpace = Go(spaceNum, lineData[0], int(lineData[2]))
                #Property Space
                elif idChar == 'P':
                    priceList = []
                    rentList = []
                    for i in range(2, 5):
                        priceList.append(int(lineData[i]))
                    for i in range(5, 11):
                        rentList.append(int(lineData[i]))
                    newSpace = Property(spaceNum, lineData[0], priceList, rentList, lineData[11])
                #Community Chest Space
                elif idChar == 'C':
                    newSpace = CommunityChest(spaceNum, lineData[0])
                #Tax Space
                elif idChar == 'T':
                    newSpace = Tax(spaceNum, lineData[0], int(lineData[2]), int(lineData[3]))
                #Railroad Space
                elif idChar == 'R':
                    priceList = []
                    rentList = []
                    for i in range(2, 4):
                        priceList.append(int(lineData[i]))
                    for i in range(4, 8):
                        rentList.append(int(lineData[i]))
                    newSpace = Railroad(spaceNum, lineData[0], priceList, rentList)
                #Chance Space
                elif idChar == 'H':
                    newSpace = Chance(spaceNum, lineData[0])
                #Jail Space
                elif idChar == 'J':
                    newSpace = Jail(spaceNum, lineData[0], int(lineData[2]), int(lineData[3]))
                #Utility Space
                elif idChar == 'U':
                    priceList = []
                    rentList = []
                    for i in range(2, 4):
                        priceList.append(int(lineData[i]))
                    for i in range(4, 6):
                        rentList.append(int(lineData[i]))
                    newSpace = Utility(spaceNum, lineData[0], priceList, rentList)
                #Free Parking Space
                elif idChar == 'F':
                    newSpace = FreeParking(spaceNum, lineData[0])
                #Go To Jail Space
                elif idChar == '2':
                    newSpace = GoToJail(spaceNum, lineData[0])
                #Invalid Space ID
                else:
                    print("Invalid Space identifier character: " + idChar)
                    exit(0)

                #If the space was successfully created, we add it to self.spaces
                try:
                    newSpace
                except NameError:
                    print("newSpace was not defined.")
                else:
                    self.spaces.append(newSpace)

def main():
    theBoard = Board()

main()