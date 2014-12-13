//Created by Ryan Branch

#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
#include <ctime>

using namespace std;

class Space {
	public:
		Space();
		Space(char spaceType, int positionIndex, string spaceName);
	private:
		char spaceType;
		int positionIndex;
		string spaceName;
};

Space::Space() {
	
	return;
}

Space::Space(char spaceType, int positionIndex, string spaceName) {
	this->spaceType = spaceType;
	this->positionIndex = positionIndex;
	this->spaceName = spaceName;
	
	return;
}

class Property : public Space { // Derived from Space
	public:
		Property();
		Property(int price, vector<int> rents, char spaceChar, int positionNum, string spaceID);
	private:
		int owner;
		int price;
		int numHouses;
		vector<int> rents;
		bool hasHotel;
};

Property::Property() {
	owner = -1;
	numHouses = 0;
	hasHotel = false;
	return;
}

Property::Property(int price, vector<int> rents, char spaceChar, int positionNum, string spaceID)
	: Space(spaceChar, positionNum, spaceID)
{
	this->price = price;
	this->rents = rents;
	owner = -1;
	numHouses = 0;
	hasHotel = false;
	return;
}

class Tax : public Space { // Derived from Space
	public:
		Tax();
		Tax(int taxRent, char spaceChar, int positionNum, string spaceID);
	private:
		int taxRent;
};

Tax::Tax() {
	
	return;
}

Tax::Tax(int taxRent, char spaceChar, int positionNum, string spaceID)
	: Space(spaceChar, positionNum, spaceID)
{
	this->taxRent = taxRent;
	return;
}

class Railroad : public Space { // Derived from Space
	public:
		Railroad();
		Railroad(int price, vector<int> railroadRents, char spaceChar, int positionNum, string spaceID);
	private:
		int owner;
		int price;
		vector<int> railroadRents;
};

Railroad::Railroad() {
	owner = -1;
	return;
}

Railroad::Railroad(int price, vector<int> railroadRents, char spaceChar, int positionNum, string spaceID)
	: Space(spaceChar, positionNum, spaceID)
{
	this->price = price;
	this->railroadRents = railroadRents;
	owner = -1;
	return;
}

class Utility : public Space { // Derived from Space
	public:
		Utility();
		Utility(int price, vector<int> rollRents, char spaceChar, int positionNum, string spaceID);
	private:
		int owner;
		int price;
		vector<int> rollRents;
};

Utility::Utility() {
	owner = -1;
	return;
}

Utility::Utility(int price, vector<int> rollRents, char spaceChar, int positionNum, string spaceID)
	: Space(spaceChar, positionNum, spaceID)
{
	this->price = price;
	this->rollRents = rollRents;
	owner = -1;
	return;
}

class Player {
	public:
		Player();
	private:
		
};

Player::Player() {
	
	return;
}

int RollDie() {
	int roll = ((rand() % 6) + 1) + ((rand() % 6) + 1);
	return roll;
}

int MovePlayer(int position) {
	position = (position + RollDie()) % 40;
	return position;
}

vector<int> SeedDeck(vector<int> deck, int numSeeds) {
	int i;
	bool seeded;
	int deckPos;
	for (i = 1; i <= numSeeds; i++) {
		seeded = false;
		while (!seeded) {
			deckPos = (rand() % deck.size());
			if (deck[deckPos] == 0) {
				deck[deckPos] = i;
				seeded = true;
			}
		}
	}	
	return deck;
}

int takeFromDeck(vector<int> &deck) {
	int card;
	int i;
	card = deck[0];
	for (i = 0; i < (deck.size() - 1); i++) {
		deck[i] = deck[i+1];
	}
	deck.back() = card;
	return card;
}

int DoCC(int card, int pos) {
	switch(card){
		case 1:
			pos = 0;
			break;
		case 2:
			pos = 10;
	}
	return pos;
}

int DoCh(int card, int pos) {
	switch(card){
		case 1:
			pos = 0;
			break;
		case 2:
			pos = 24;
		case 3:
			pos = 11;
			break;
		case 4:
			if ((pos >= 12) && (pos < 28)) {
				pos = 28;
			}
			else {
				pos = 12;
			}
			break;
		case 5:
			if ((pos >= 5) && (pos < 15)) {
				pos = 15;
			}
			else if ((pos >= 15) && (pos < 25)) {
				pos = 25;
			}
			else if ((pos >= 25) && (pos < 35)) {
				pos = 35;
			}
			else {
				pos = 5;
			}
			break;
		case 6:
			pos -= 3;
		case 7:
			pos = 10;
			break;
		case 8:
			pos = 5;
		case 9:
			pos = 39;
	}
	return pos;
}

vector<int> PlayGame(int turnsToRun) {
	vector<int> spaceFrequencies(40, 0);
	vector<int> chanceDeck(16, 0);
	vector<int> communityChestDeck(16, 0);
	int playerPos = 0;
	int cardDrawn;
	int i;
	int j;
	int k;

	chanceDeck = SeedDeck(chanceDeck, 9);
	communityChestDeck = SeedDeck(communityChestDeck, 2);
	
	for (i = 0; i < turnsToRun; i++) {
		playerPos = MovePlayer(playerPos);
		
		if (playerPos == 30) {
			playerPos = 10;
		}
		else if ((playerPos == 2) || (playerPos == 17) || (playerPos == 33)) {
			cardDrawn = takeFromDeck(communityChestDeck);
			playerPos = DoCC(cardDrawn, playerPos);
		}
		else if ((playerPos == 7) || (playerPos == 22) || (playerPos == 36) ) {
			cardDrawn = takeFromDeck(chanceDeck);
			playerPos = DoCh(cardDrawn, playerPos);
		}
		
		spaceFrequencies[playerPos]++;
		
	}
	return spaceFrequencies;
}

vector<Space> getBoard() {
	const string BOARD_FILE = "board.txt";
	ifstream inBoard;
	vector<int> spaceRents;
	Space newSpace;
	string nameOfSpace;
	char typeOfSpace;
	int purchasePrice;
	int spaceRent;
	int spacePos;
	vector<Space> gameBoard;
	int i;

	inBoard.open(BOARD_FILE.c_str());

	spacePos = 0;
	while (!inBoard.eof()) {
		inBoard >> nameOfSpace;
		//Ignores any trailing whitespace at the end of the file
		if (!nameOfSpace.empty()) {
			inBoard >> typeOfSpace;
			//Handles each designated type of space, shown in order of appearance on the official game board.
			switch(typeOfSpace){
				//Property
				case 'P':
					inBoard >> purchasePrice;
					for (i = 0; i < 7; i++) {
						inBoard >> spaceRent;
						spaceRents.push_back(spaceRent);
					}
					newSpace = Property(purchasePrice, spaceRents, typeOfSpace, spacePos, nameOfSpace);
					break;
				//Tax
				case 'T':
					inBoard >> spaceRent;
					newSpace = Tax(spaceRent, typeOfSpace, spacePos, nameOfSpace);
					break;
				//Railroad
				case 'R':
					inBoard >> purchasePrice;
					for (i = 0; i < 4; i++) {
						inBoard >> spaceRent;
						spaceRents.push_back(spaceRent);
					}
					newSpace = Railroad(purchasePrice, spaceRents, typeOfSpace, spacePos, nameOfSpace);
					break;
				//Utility
				case 'U':
					inBoard >> purchasePrice;
					for (i = 0; i < 2; i++) {
						inBoard >> spaceRent;
						spaceRents.push_back(spaceRent);
					}
					newSpace = Utility(purchasePrice, spaceRents, typeOfSpace, spacePos, nameOfSpace);
					break;
				//"Go" (G), "Community Chest" (C), "Chance" (H), "Jail" (J), "Free Parking" (F), or "Go to Jail" (2)
				default:
					newSpace = Space(typeOfSpace, spacePos, nameOfSpace);
			}
			nameOfSpace.clear(); //Clears nameOfSpace for the next iteration
			spacePos++; //Increments board position index for the next property
		}
	}
	inBoard.close();
	return gameBoard;
}

int main() {
	ofstream outFS;
	srand(time(0));
	int numPlayers;
	int i;
	vector<Player> players;
	vector<Space> board;
	string filename;
	
	cout << "Please enter the number of players to simulate." << endl;
	cin >> numPlayers;
	cout << "Please enter the name of the output .csv file to be generated." << endl;
	cin >> filename;
	filename += ".csv";
	
	board = getBoard();
	
	for (i = 0; i < numPlayers; i++) {
	
	}
	
	outFS.open(filename.c_str());

	outFS.close();
	return 0;
}