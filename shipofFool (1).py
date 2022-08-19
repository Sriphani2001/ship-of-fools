import random
from typing import List


class Die:
    """a 6 faced die has 6 values 1-6
       so random integers should be 6    """
    def __init__(self):
        self.die_value = None
        
    def roll(self) -> None:
        """obtain a random value in values of 1 to 6
        """
        random_int = random.randint(1,6)
        self.die_value = random_int
        
    def get_value(self) -> int:
        """return the value of random integer
        like rolling and obtaining a value from die
        """
        return self.die_value


class DiceCup:
    """ in game dice cup will have 5 dice
    so we will rolling dice for 5 times and get those values.
    """
    def __init__(self) -> None:
        self.roll_dice = []
        self.banked_dice = []
        self.op_values = []
        self.put_die_in_dice()
        
    def value(self, index: int) -> int:
        """obtain a particular die value by index

        Args:index (int): Index of die in dice (0-4)

        Returns:int : the value of the die which index was passed
        """
        return self.roll_dice[index].get_value() 
    
    def put_die_in_dice(self) -> None:
        """create a list and add output values to list
        """
        for i in range(5):
            die = Die()
            self.roll_dice.append(die)
            
   
    
    def bank(self, index: int) -> None:
        """Bank a die in dice list by its index

        Args:
            index (int): Index of die in dice (0-4)
        """
        self.banked_dice.append(self.roll_dice[index])
        
    def is_banked(self, index: int) -> bool:
        """verify if a die is unbanked or banked
        Args:index (int): Index of die in dice (0-4)

        Returns: bool: If the die is banked then return true, else return false
        """
        if self.roll_dice[index] not in self.banked_dice:
            return False
        return True
    
    def release(self, index: int) -> None:
        """realease the banked die by its index

        Args:
            index (int): Index of die in dice (0-4)
        """
        self.banked_dice.remove(self.roll_dice[index])
        
    def release_all(self) -> None:
        """realese all the banked dice
        """
        self.banked_dice = []
        
    def roll(self) -> None:
        """Roll the dice
        """
        self.op_values = []
        for die in self.roll_dice:
            if die not in self.banked_dice:
                die.roll()
                self.op_values.append(die.get_value())
                
    def get_rolled_result(self) -> List:
        """return all the values after rolling dice to form list
            List: List of dice values
        """
        return self.op_values
    
    
class ShipOfFoolsGame:
    """This class is a main and Core Game Logic.
    it provides working of game"""    

    def __init__(self, winning_score: int) -> None:
        """ The class attributes are initialized

        Args:
            winning_score (int): [It is the highest value to win the game, 
                                  If a player reach the winning score, 
                                  the game will over and who reaches it will be winner]
        """

        self.d_cup = DiceCup()
        self.winningscore = winning_score
        self.no_of_roll_allowed = 3
        self.status_game = [False, False, False]
        self._score = 0
        
    def round(self, player_name: str) -> None:
        """In game the player has 3 chances to throw cup of dice.
        In every chances player roll the unbanked dices and get a score.

        Args: player_name (str): [identification of player]
        """
        
        self.__init__(21)   # Initialize all values for new round!
        
        print(f"{player_name} turn: \nHis results")
        
        while self.no_of_roll_allowed>0:
            self.d_cup.roll()
            values = self.d_cup.get_rolled_result()
            self.print_values(values)
            self.evalute(values)
            self.no_of_roll_allowed = self.no_of_roll_allowed-1
            
    def evalute(self, values: List) -> None:
        """The fuction evalute the rolled dice. It check if the dices has ship, captain and crew or not. 

        Args:
            values (List): [Resultant values or rolled dices]

        Returns:
            [type]: [None]
        """
        
        if self.status_game[0] == False:    # If We don't have the ship
            if 6 in values:
                self.status_game[0] = True
                self.d_cup.bank(0)
                values.remove(6)
            else:
                return # break the method because we dont even have the ship
            
        if self.status_game[1] == False:    # We have ship but we don't have the captain
            if 5 in values:
                self.status_game[1] = True
                self.d_cup.bank(1)
                values.remove(5)
            else:
                return # break the method because we dont have the captain
            
        if self.status_game[2] == False:    # We have ship and captain but we don't have the crew
            if 4 in values:
                self.status_game[2] = True
                self.d_cup.bank(2)
                values.remove(4)
            else:
                return # break the method because we dont have the crew
            
        # We are here, that means the ship, captain and crew are availabe. Now we looking for the scores
        self._score = sum(values)
            
    def get_score(self) -> int:
        """Get the current round score

        Returns:
            int: current round score
        """
        return self._score
    
    def get_winning_score(self) -> int:
        """get wiining score

        Returns:
            int: winning score
        """
        return self.winningscore
    
    def print_values(self, values: List) -> None:
        """print the values after rolling the dices

        Args:
            values (List): vallues of rolled dices
        """
        all_values = []
        value = 6
        # The dices who are not rolled, If find 6 in previous chances, we keep this dice.
        for i in range (3):
            if self.status_game[i] == True:
                all_values.append(value)
                value -= 1
            else: break
        # the dices who are rolled 
        for val in values:
            all_values.append(val)
        print(all_values) 


class Player:
    """
        Player class provides  all the attributes and methods of a player.
        Player can play game.
        A player has a name and score attribute
        A player has a play role (method)
    """
    
    def __init__(self) -> None:
        self._name = None
        self._score = 0     # Obtained total score for a player
        
    def set_name(self, name: str) -> None:
        self._name = name
        
    def get_name(self) -> str:
        return self._name
        
    def current_score(self) -> int:
        return self._score
    
    def reset_score(self) -> None:
        self._score = 0
    
    def play_round(self, game: ShipOfFoolsGame)  -> None:
        """Player play rounds to gain winning scores

        Args:
            game (ShipOfFoolsGame): The Playing Game object
        """
        
        game.round(self._name)
        print(f"In this round you scored: {game.get_score()}")
        self._score += game.get_score()
        return
    


class PlayRoom:
    """
        In this room multiple player are added. And Play their game.
        The room will track all the player score and controll the game.
    """
    
    def __init__(self) -> None:
        self._game = None
        self._players = []
        self._winner = None
    
    def set_game(self, game: ShipOfFoolsGame) -> None:
        """set the game

        Args:
            game (ShipOfFoolsGame): Game object, will be played by the players. 
        """
        self._game = game
    
    def add_player(self, player: Player) -> None:
        """Add player to this room

        Args:
            player (Player): player object, who play the game
        """
        self._players.append(player)
    
    def reset_scores(self) -> None:
        """reset scores of the player who is added in this room.
        """
        for player in self._players:
            player.reset_score()

    def play_round(self) -> None:
        """In a round every player will have 3 chances to get a highest score.
        """
        for player in self._players:
            player.play_round(self._game)
    
    def game_finished(self) -> bool:
        """verify that the game is finished or not.

        Returns:bool: return True, if the game completed, else return false.
        """
        for player in self._players:
            if player.current_score() >= self._game.get_winning_score():
                self._winner = player
                return True
        return False
    
    def print_scores(self) -> None:
        """Print all player's score details.
        """
        for player in self._players:
            print(f"{player.get_name()}'s score: {player.current_score()}")
    
    def print_winner(self) -> None:
        """The winner of the game prints!"""
        print(f"Hey!! Congratulations {self._winner.get_name()}! You won the match!")
        


if __name__ =="__main__":
    """
        The main loop of the game ship of fools is to
        create a playroom, create a game instances
        create player instances, add game and players in playroom
        loop the game until the game finished
    """
    room = PlayRoom()
    game = ShipOfFoolsGame(21)
    room.set_game(game)
    player1 = Player()
    player1.set_name("mr d")
    player2 = Player()
    player2.set_name("mr p")
    room.add_player(player1)
    room.add_player(player2)
    room.reset_scores()
    while not room.game_finished():
        room.play_round()
        room.print_scores()
    room.print_winner()