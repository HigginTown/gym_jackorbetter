import treys
import gym
from gym import spaces
from gym.utils import seeding
from gym import error, spaces, utils
from gym.utils import seeding

class JacksEnvironment(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        self.action_space = spaces.Discrete(26) # 5 choose 3,  plus 5 choose 2,  plus 5, plus 1
        self.observation_space = spaces.Discrete(2598960) # number of five card hand combos
        self.deck = treys.Deck()
        self.hand = self.deal_hand()
        # self.done = False
        self.evaluator = treys.Evaluator()
        
        # SET THE REWARDS
        self.RANK_CLASS_STRING_TO_REWARD = {
            'Straight Flush': 100,
            'Four of a Kind': 25,
            'Full House': 9,
            'Flush': 6,
            'Straight': 4,
            'Three of a Kind': 3,
            'Two Pair': 2,
            'Pair': 1, 
            'High Card': -1}
        
        self.RANK_CLASS_TO_STRING = {
        1: "Straight Flush",
        2: "Four of a Kind",
        3: "Full House",
        4: "Flush",
        5: "Straight",
        6: "Three of a Kind",
        7: "Two Pair",
        8: "Pair",
        9: "High Card"
    }

        # get the hand rank for jacks 
        # so we can later check if the player hand is better than jacks 
        self._jacks_hand_score = self.evaluator.evaluate( [
                                                        treys.Card.new('Jh'), 
                                                        treys.Card.new('Js'), 
                                                        treys.Card.new('2s')
                                                        ],
                                                        [
                                                        treys.Card.new('3h'), 
                                                        treys.Card.new('4d')
                                                        ]
                                                    )
    
    def deal_hand(self):
        hand = self.deck.draw(5)
        hand.sort()
        return hand
        
    def _get_obs(self):
        return self.hand
    
    def reset(self):
        self.deck = treys.Deck()
        self.hand = self.deal_hand()
            
    
    def exchange_cards(self, index_positions):
        # accept the index positions of the new cards 
        # and remove them from the list 

        if index_positions == [999]: # special case for None
            return 
        
        # remove the elements from the list, starting with the highest index position
        
        for card in sorted(index_positions, reverse = True):
            del self.hand[card]
        
        # get the new cards
        new_cards = self.deck.draw(len(index_positions))
        
        if type(new_cards) != list: new_cards = [new_cards]
        
        # create the new hand
        new_hand = self.hand + new_cards
        self.hand = new_hand
        
        
    def render(self, mode='human', close=False):
        pass

        
    def get_reward(self):
        score = self.evaluator.evaluate(self.hand[:3], self.hand[3:])
        class_name = self.RANK_CLASS_TO_STRING[self.evaluator.get_rank_class(score)]
        
        # compare to the jacks
        if score > self._jacks_hand_score: return -1
        else:
            reward = self.RANK_CLASS_STRING_TO_REWARD[class_name]
            return reward
        
        
    def step(self, action):
        # make a choice to replace cards in the hand
        replacements = action
        self.exchange_cards(replacements)
        r = self.get_reward()
        
        # return the tuple for the step function
        # self.done = True
        ret = self._get_obs(), r, True, {}
        self.reset()
        # print(ret)
        return ret
        