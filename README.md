# Jacks or Better Poker Gym Environment



#### ACTION SPACE

SINCE THERE ARE FIVE CARDS AND THE PLAYER CAN DISCARD

- Any of 3 cards = 5 choose 3 = 10
- Any of 2 cards = 5 choose 2 = 10
- Any 1 card     = 5 choose 1 = 5
- No cards                    = 1

TOTAL is 26 Possible Actions for each hand


#### OBSERVATION SPACE 

The observation space is any 5 card hand a player can make from the 52 card deck 

52 cards, 5 card hand = 52 choose 5 = 2598960

