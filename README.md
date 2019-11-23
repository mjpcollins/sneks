# Sneks

This is a project to simulate a drinking game that was invented with a few friends and 
myself at university. 

Many drinking games appear to rely more on luck than skill to get people drunk. I
suppose this is a good thing, as it introduces chaos to pre-drinks rather than one 
person ending up sober due to skill and others wasted because they're new.

Therefore, Snakes and Ladders is a wonderful candidate for a drinking game. The game
is based entirely on luck and has basic rules which allows for easy addition of
new drinking rules. 

However, it is recognised that the lack of any skill based interaction is a flaw,
so we introduce rock-paper-scissors based challenges and the ability to choose 
who drinks to correct this.

This project focuses on configuring the Snakes and Ladders locations to 
optimise the drunkness of the participants.  
 

### General Rules

Every turn, you roll either a die or some dice. The ultimate aim is to win, 
the side affect is getting quite drunk.

To win, you must get to square 100. If you overshoot, you bounce. 
For clarification, if one is on square 98 and they roll a 5, they
will overshoot 100 and bounce back to square 97.

If you land on a snake head, you must follow the snake to wherever its tail lands.

If you land on a ladder, you must climb to wherever the tip of the ladder is located.  

### The Drinking Rules

There are 3 basic rules that dictate when you should drink.

1. If you are overtaken by another player, you must take  a drink
2. If you manage to move up a level (e.g., 9 -> 11 or 26 -> 32), you can instruct another player to take a drink
3. If you land on the same space as another player you must play rock-paper-scissors (RPS) with them. The winner moves directly up (e.g., 33 -> 43, 55 -> 65), and the loser directly down (e.g., 99 -> 89, 14 -> 4)

All interactions between the rules must be observed. If you land on a ladder
and overtake many people, they must all drink in addition to allowing
you to dictate people to drink. When you move up a level from winning a RPS challenge,
you are again allowed to dictate someone to drink.

### Classes

There are two main classes driving all interactions. An AI class and a Board class.

The AI class keeps track of all personal things. Location, drinks, movement.

The Board class oversees the chaos and reports on the progress of the game.

The simulate a game, create some AI objects and then add them to the board.
Run Board.take_turn() a few times to see how it progresses. 