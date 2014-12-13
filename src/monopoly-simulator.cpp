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
	private:
		
};

Property::Property() {
	
	return;
}

class Railroad : public Space { // Derived from Space
	public:
		Railroad();
	private:
		
};

Railroad::Railroad() {
	
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

int main() {
	int i;
	int j;
	const string BOARD_FILE = "board.txt";
	ifstream inBoard;
	ofstream outFS;
	srand(time(0));
	int numPlayers;
	string filename;
	string nameOfSpace;
	char typeOfSpace;
	int purchasePrice;
	int rent;
	vector<int> rents;
	
	vector<Player> players;
	vector<Space> board;
	
	cout << "Please enter the number of players to simulate." << endl;
	cin >> numPlayers;
	cout << "Please enter the name of the output .csv file to be generated." << endl;
	cin >> filename;
	filename += ".csv";
	inBoard.open(BOARD_FILE.c_str());
	
	i = 0;
	while (!inBoard.eof()) {
		inBoard >> nameOfSpace;
		//Ignores any trailing whitespace at the end of the file
		if (!nameOfSpace.empty()) {
			inBoard >> typeOfSpace;
			//Handles each designated type of space, shown in order of appearance on the official game board.
			switch(typeOfSpace){
				//Go
				case 'G':
					
					break;
				//Property
				case 'P':
					
					break;
				//Community Chest
				case 'C':
					
					break;
				//Tax
				case 'T':
					
					break;
				//Railroad
				case 'R':
					
					break;
				//cHance
				case 'H':
					
					break;
				//Jail
				case 'J':
					
					break;
				//Utility
				case 'U':
					
					break;
				//Free Parking
				case 'F':
					
					break;
				//Go "2" Jail
				case '2':
					
					break;
			}
			nameOfSpace.clear(); //Clears nameOfSpace for the next iteration
			i++; //Increments board position index for the next property
		}
	}
	inBoard.close();
	
	for (i = 0; i < numPlayers; i++) {
	
	}
	
	outFS.open(filename.c_str());

	outFS.close();
	return 0;
}