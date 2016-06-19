//Created by Ryan Branch

#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
#include <ctime>

using namespace std;

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
			break;
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
	bool secondLastDubs = false;
	bool lastDubs = false;
	bool currentDubs = false;
	bool inJail = false;
	int jailTurnsLeft = 0;
	chanceDeck = SeedDeck(chanceDeck, 9);
	communityChestDeck = SeedDeck(communityChestDeck, 2);
	for (i = 0; i < turnsToRun; i++) {
		int roll1 = (rand() % 6) + 1;
		int roll2 = (rand() % 6) + 1;
		
		//Checks for rolling the same number twice, AKA "doubles" or "dubs"
		if (roll1 == roll2) {
			currentDubs = true;
			
			//If you're not in jail and your last 3 rolls are dubs, you go to jail
			if ((!(inJail)) && ((lastDubs) && (secondLastDubs))) {
				playerPos = 10;
				inJail = true;
				
				//This jailTurnsLeft is set to 3, and not 2, due to control flow management
				jailTurnsLeft = 3;
				
				//Ensures that rolling 4 dubs in a row doesn't count as 2 sets of 3 dubs in a row
				currentDubs = false;
			}
				
			//If you are in jail and you roll dubs, you get out of jail
			else if (inJail) {
				inJail = false;
				jailTurnsLeft = 0;
			}
		}
		
		//If you're not in jail, you move normally and check conditions
		if (!(inJail)) {
			//move
			playerPos += (roll1 + roll2);
			playerPos = playerPos % 40;
			
			//check conditions
			if (playerPos == 30) {
				playerPos = 10;
				inJail = true;
				
				//This jailTurnsLeft is set to 2, and not 3, due to control flow management
				jailTurnsLeft = 2;
			}
			else if ((playerPos == 2) || (playerPos == 17) || (playerPos == 33)) {
				cardDrawn = takeFromDeck(communityChestDeck);
				playerPos = DoCC(cardDrawn, playerPos);
			}
			else if ((playerPos == 7) || (playerPos == 22) || (playerPos == 36) ) {
				cardDrawn = takeFromDeck(chanceDeck);
				playerPos = DoCh(cardDrawn, playerPos);
			}
		}
		else {
			if (jailTurnsLeft == 0) {
				playerPos += (roll1 + roll2);
				playerPos = playerPos % 40;
				inJail = false;
				jailTurnsLeft = 0;
			}
			else {
				jailTurnsLeft--;
			}
		}
		
		spaceFrequencies[playerPos]++;
		secondLastDubs = lastDubs;
		lastDubs = currentDubs;
		currentDubs = false;
	}
	return spaceFrequencies;
}

int main() {
	int turnsPerGame;
	int gamesPerSim;
	string filename;
	vector<int> currentFrequencies;
	vector<double> totalFrequencies(40, 0);
	ofstream outFS;
	int sumOfFrequencies = 0;
	int i;
	int j;
	srand(time(0));
	cout << "Please enter the desired duration of each game, in turns." << endl;
	cin >> turnsPerGame;
	cout << "Please enter the desired number of games to simulate." << endl;
	cin >> gamesPerSim;
	cout << "Please enter the name of the output .csv file to be generated." << endl;
	cin >> filename;
	filename += ".csv";
	for (i = 0; i < gamesPerSim; i++) {
		currentFrequencies = PlayGame(turnsPerGame);
		for (j = 0; j < currentFrequencies.size(); j++) {
			totalFrequencies[j] += currentFrequencies[j];
		}
	}
	outFS.open(filename.c_str());
	outFS << "Space, Frequency" << endl;
	for (i = 0; i < totalFrequencies.size(); i++) {
		outFS << i << ", " << totalFrequencies[i] << endl;
	}
	outFS.close();
	return 0;
}