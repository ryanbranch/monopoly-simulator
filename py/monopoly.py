import random
import shlex

#Game parameters
NUM_PLAYERS = 4
NUM_GAMES = 1

#File paths
BOARD_FILE = "board.txt"
COMMUNITYCHEST_FILE = "communitychest.txt"
CHANCE_FILE = "chance.txt"

#Card represents a card which is drawn upon landing on a CommunityChest or Chance space
class Card:
    def __init__(self, desc_):
        self.desc = desc_

#Represents a card which causes a player to move to a space as they would normally
class MoveNormal(Card):
    def __init__(self, location_, desc_):
        Card.__init__(self, desc_)
        self.location = location_

#Represents a card which causes a player to move to the nearest utility
#If the utility is owned, the player must roll the dice and pay the owner 10x the dice roll
class MoveUtility(Card):
    def __init__(self, multiplier_, locations_, desc_):
        Card.__init__(self, desc_)
        self.multiplier = multiplier_
        self.locations = locations_

#Represents a card which causes a player to move to the nearest railroad
#If the railroad is owned, the player must pay the owner 2x the amount owed
class MoveRailroad(Card):
    def __init__(self, multiplier_, locations_, desc_):
        Card.__init__(self, desc_)
        self.multiplier = multiplier_
        self.locations = locations_

#Represents a card which causes a player to move back a given number of spaces
class MoveBack(Card):
    def __init__(self, amount_, desc_):
        Card.__init__(self, desc_)
        self.amount = amount_

#Represents a card which causes a player to receive money from the bank
class FromBank(Card):
    def __init__(self, amount_, desc_):
        Card.__init__(self, desc_)
        self.amount = amount_

#Represents a card which causes a player to pay a static amount of money to the bank
class ToBank(Card):
    def __init__(self, amount_, desc_):
        Card.__init__(self, desc_)
        self.amount = amount_

#Represents a card which causes a player to go to jail
class ToJail(Card):
    def __init__(self, location_, desc_):
        Card.__init__(self, desc_)
        self.location = location_

#Represents a card which lets a player get out of jail for free
class OutJail(Card):
    def __init__(self, desc_):
        Card.__init__(self, desc_)

#Represents a card which causes a player to receive money from each player
class FromPlayers(Card):
    def __init__(self, amount_, desc_):
        Card.__init__(self, desc_)
        self.amount = amount_

#Represents a card which causes a player to pay money to each player
class ToPlayers(Card):
    def __init__(self, amount_, desc_):
        Card.__init__(self, desc_)
        self.amount = amount_

#Represents a card which causes a player to pay money to the bank on a per house/hotel basis
class PerHouse(Card):
    def __init__(self, amountHouse_, amountHotel_, desc_):
        Card.__init__(self, desc_)
        self.amountHouse = amountHouse_
        self.amountHotel = amountHotel_

#Space represents any space on the board where a player can land
class Space:
    def __init__(self, location_, name_):
        self.location = location_
        self.name = name_
        self.hasOwner = False
        self.owner = -1

    def __str__(self):
        return self.name

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
        self.numSpaces = 0

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
                    self.numSpaces += 1

            #Closes boardFile
            boardFile.close()

class Player:

    def __init__(self, name_):
        self.name = name_
        self.location = 0
        self.money = 1500
        self.outJailCards = 0
        self.inGame = True

    def __str__(self):
        return self.name

    def rollDice(self):
        roll1 = random.randint(1,6)
        roll2 = random.randint(1,6)
        return roll1 + roll2

class Strategy:

    def __init__(self):
        pass


class Game:
    def __init__(self):
        self.players = []
        for i in range(NUM_PLAYERS):
            self.players.append(Player("Player " + str(i)))
        self.playersRemaining = NUM_PLAYERS

    def playersRemain(self):
        numRemaining = 0
        for player in self.players:
            if player.inGame:
                numRemaining += 1
        return numRemaining >= 2

    def takeChance(self, player):
        pass

    def takeChest(self, player):
        pass

    def moveNormal(self, player, destination):
        pass

    def fromBank(self, player, amount):
        pass

    def toBank(self, player, amount):
        pass

    def toJail(self, player):
        pass

    def outJail(self, player):
        pass

    def toPlayers(self, player, amount):
        pass

    def moveUtility(self, player, destination, multiplier):
        pass

    def moveRailroad(self, player, destination, multiplier):
        pass

class Container:

    def __init__(self):
        #initialize the board
        self.board = Board()

        #Initialize and build the card decks
        self.chanceDeck = []
        self.buildChance()
        self.chestDeck = []
        self.buildChest()

    def runGame(self):
        self.currentGame = Game()
        while self.currentGame.playersRemaining >= 2:
            for player in self.currentGame.players:

                #Move player to a new location based on 2 rolls of 6 sided dice
                player.location += player.rollDice()
                if player.location >= self.board.numSpaces:
                    player.location = player.location % self.board.numSpaces

                #Evaluate actions based on the strategy for this new location
                #Check if the space is owned
                if not self.board.spaces[player.location].hasOwner:
                    pass

    def buildChance(self):
        with open(CHANCE_FILE, 'r') as chanceFile:
            for cardNum, line in enumerate(chanceFile):
                lineData = shlex.split(line)

                #Builds self.spaces conditionally based on the value of lineData[0]
                idStr = lineData[0]

                #Creates the space newSpace based on lineData and adds it to self.spaces
                #MoveNormal Card
                if idStr == 'MN':
                    newCard = MoveNormal(int(lineData[1]), lineData[-1])
                #MoveUtility
                elif idStr == 'MU':
                    locList = [int(lineData[2]), int(lineData[3])]
                    newCard = MoveUtility(int(lineData[1]), locList, lineData[-1])
                #MoveRailroad
                elif idStr == 'MR':
                    locList = [int(lineData[2]), int(lineData[3]), int(lineData[4]), int(lineData[5])]
                    newCard = MoveRailroad(int(lineData[1]), locList, lineData[-1])
                #MoveBack
                elif idStr == 'MB':
                    newCard = MoveBack(int(lineData[1]), lineData[-1])
                #FromBank
                elif idStr == 'FB':
                    newCard = FromBank(int(lineData[1]), lineData[-1])
                #ToBank
                elif idStr == 'TB':
                    newCard = ToBank(int(lineData[1]), lineData[-1])
                #ToJail
                elif idStr == 'TJ':
                    newCard = ToJail(int(lineData[1]), lineData[-1])
                #OutJail
                elif idStr == 'OJ':
                    newCard = OutJail(lineData[-1])
                #FromPlayers
                elif idStr == 'FP':
                    newCard = FromPlayers(int(lineData[1]), lineData[-1])
                #ToPlayers
                elif idStr == 'TP':
                    newCard = ToPlayers(int(lineData[1]), lineData[-1])
                #PerHouse
                elif idStr == 'PH':
                    newCard = PerHouse(int(lineData[1]), int(lineData[2]), lineData[-1])
                else:
                    print("Invalid Space identifier string: " + idStr)
                    exit(0)

                #If the card was successfully created, we add it to the respective deck
                try:
                    newCard
                except NameError:
                    print("newCard was not defined.")
                else:
                    self.chanceDeck.append(newCard)
                    print("Card added to CHANCE deck.")

            #Closes chanceFile
            chanceFile.close()

    def buildChest(self):
        with open(COMMUNITYCHEST_FILE, 'r') as chestFile:
            for cardNum, line in enumerate(chestFile):
                lineData = shlex.split(line)

                #Builds self.spaces conditionally based on the value of lineData[0]
                idStr = lineData[0]

                #Creates the space newSpace based on lineData and adds it to self.spaces
                #MoveNormal Card
                if idStr == 'MN':
                    newCard = MoveNormal(int(lineData[1]), lineData[-1])
                #MoveUtility
                elif idStr == 'MU':
                    locList = [int([lineData[2]]), int(lineData[3])]
                    newCard = MoveUtility(int(lineData[1]), locList, lineData[-1])
                #MoveRailroad
                elif idStr == 'MR':
                    locList = [int([lineData[2]]), int(lineData[3]), int([lineData[4]]), int(lineData[5])]
                    newCard = MoveRailroad(int(lineData[1]), locList, lineData[-1])
                #MoveBack
                elif idStr == 'MB':
                    newCard = MoveBack(int(lineData[1]), lineData[-1])
                #FromBank
                elif idStr == 'FB':
                    newCard = FromBank(int(lineData[1]), lineData[-1])
                #ToBank
                elif idStr == 'TB':
                    newCard = ToBank(int(lineData[1]), lineData[-1])
                #ToJail
                elif idStr == 'TJ':
                    newCard = ToJail(int(lineData[1]), lineData[-1])
                #OutJail
                elif idStr == 'OJ':
                    newCard = OutJail(lineData[-1])
                #FromPlayers
                elif idStr == 'FP':
                    newCard = FromPlayers(int(lineData[1]), lineData[-1])
                #ToPlayers
                elif idStr == 'TP':
                    newCard = ToPlayers(int(lineData[1]), lineData[-1])
                #PerHouse
                elif idStr == 'PH':
                    newCard = PerHouse(int(lineData[1]), int(lineData[2]), lineData[-1])
                else:
                    print("Invalid Space identifier string: " + idStr)
                    exit(0)

                #If the card was successfully created, we add it to the respective deck
                try:
                    newCard
                except NameError:
                    print("newCard was not defined.")
                else:
                    self.chestDeck.append(newCard)
                    print("Card added to COMMUNITY CHEST deck.")

            #Closes chestFile
            chestFile.close()

def main():
    #Sets the random seed
    random.seed(0)
    theContainer = Container()
    for i in range(NUM_GAMES):
        theContainer.runGame()

main()