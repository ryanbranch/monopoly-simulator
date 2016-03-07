monopoly location distribution
======
This program simulates a single player taking a given number of turns on the standard 2008 and beyond Monopoly board for a given number of game simulations.
It ignores any financial transactions and instead focuses solely on moving from space to space.

I wrote this program so that I could get an idea as to the probability that a player would end their turn on any given space in the game.
People have approached this problem mathematically in the past using Markov chains, however I find that to be a somewhat inappropriate approach given that monopoly games do not last anywhere near enough to an infinite amount of turns for such calculations to be truly applicable.
While they can give a good estimate, I personally believe the "brute force" approach to be more appropriate.

Upon running the program, the user is first asked to enter the number of turns for which they would like to run each game, and then the number of games that they would like to simulate.  The user is also asked to provide a name for the output file that the program generates, which is created in the .csv format.
In each game, the player is started on the "GO" space.  A 2-dice roll is generated, and the player moves that many spaces forward.  "Chance" and "Community Chest" decks are shuffled at the beginning of each game, and whenever a player lands on one of those spaces, a card is effectively drawn and movement may be carried out, according to the instructions on the card.
When the simulation completes, a file with the name specified by the user is generated, containing the cumulative frequencies that each space was landed on.

In order to fully understand the mechanism of this problem, it can be helpful to know some of the numbers that went into it.  So, I've included some of those values that were used in the calculation.  I found them on various locations of the internet.  Maybe someday I'll go through and source them all.


spaces
======
There are 40 spaces on the game board.  For the purposes of this explanation, I will refer to "GO" as space 0, and "Boardwalk" as space 39.

The following spaces cause or have the potential to cause movement when landed on by a player:
* Space 30 is the space that sends players to JAIL when landed upon.
* Spaces 2, 17, and 33 are COMMUNITY CHEST spaces.
* Spaces 7, 22, and 36 are CHANCE spaces.

The following spaces must be known in order to handle movements caused by the above spaces:
* The GO space is space 0.
* JAIL is space 10.
* Spaces 12 and 28 are utilities.
* Spaces 5, 15, 25, and 35 are railroads.
* Reading Railroad is space 5.
* St. Charles Place is space 11.
* Illinois Ave. is space 24.
* Boardwalk is space 39.

chance + community chest
======
There are 16 CHANCE cards, and 16 COMMUNITY CHEST cards.  Some of each cause movement when drawn.

The following actions can be caused by COMMUNITY CHEST cards:
* One card sends the player to the GO space
* One card sends the player to JAIL

The following actions can be caused by CHANCE cards:
* One card sends the player to the GO space
* One card sends the player to Illinois Ave.
* One card sends the player to St. Charles Place
* One card sends the player to the nearest utility (in the forward direction)
* One card sends the player to the nearest railroad
* One card sends the player back 3 spaces from their current position
* One card sends the player to JAIL
* One card sends the player to Reading Railroad
* One card sends the player to Boardwalk

restrictions
======
* Extremely high input values may lead to incorrect output due to overflow