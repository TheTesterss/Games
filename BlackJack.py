import random
import time
import json

class BlackJack:
    def __init__(self):
        self.__cards = None
        self.__state = "Default"
        self.__tookCards = [[], []]
        self.__states = []
        
    def openPacket(self):
        with open("./cards.json", "r") as file:
            self.__cards = json.load(file)
            
    def decreaseAvailability(self, name: str):
        for i in range(len(self.__cards)):
            if self.__cards[i]["name"] == name and self.__cards[i]["available"] > 0:
                self.__cards[i]["available"]-=1
            return None
        
    def revealCard(self, turn: int):
        possibilities = list(filter(lambda x: x["available"] > 0, self.__cards))
        if len(possibilities) == 0:
            self.__state = "Ended"
        try:
            card = possibilities[random.randint(0, len(possibilities) - 1)]
        except:
            card = possibilities[0]
        self.decreaseAvailability(card["name"])
        self.__tookCards[turn].append(card)
        
    def sumValues(self, turn: int):
        value = 0
        for card in self.__tookCards[turn]:
            value+=card["value"]
        return value
        
    def play(self, turn: int):
        if self.__states[turn] != "Ended":
            self.revealCard(turn=turn)
            cumule = self.sumValues(turn=turn)
            print("-----------")

            if cumule <= 21 and turn == 0:
                print(f"You got a {str(self.__tookCards[turn][-1]["value"])}. Your cumule is now: {cumule}.")
            elif cumule > 21:
                self.__state = "Ended"
                self.__states[turn] = "Ended"
                if turn == 0:
                    print(f"You got: {cumule}, You lost...")
                    print(f"System had {str(self.sumValues(turn=turn+1))} points.")
                else:
                    print(f"The system got: {cumule}, you won!")
                
            if turn == 1 and self.__states[turn] != "Ended":
                print("The system played.")
            
            time.sleep(1)
            """or (cumule > self.sumValues(turn=turn-1)) and self.__states[turn-1] == "Ended\""""
            if turn == 1 and ((cumule >= 18 and cumule <= 21)):
                print("-----------")
                self.__states[turn] = "Ended"
                print("The system concluded.")
            
    def choiceMenu(self, turn: int):
        response = None
        while not response and self.__states[turn] != "Ended":
            print("-----------")
            print("Possible words: (stop, continue).")
            choice = input("Do you continue? Or you stop now? The system will still continues: ")
            response = choice.lower()
            if response == "stop":
                if self.__tookCards[turn] == []:
                    response = None
                    print("You need to continue at least once.")
                else:
                    self.__states[turn] = "Ended"
                    break
            elif response == "continue":
                print("Alright, continuating with the next round!")
            else:
                response = None
                print("Invalid word...")
    
    def verifyStatement(self, turn: int):
        turn_1 = turn - 1 if turn == 1 else turn + 1
        if self.__states[turn] == "Ended" and self.__states[turn_1] != "Ended":
            print("-----------")
            if turn == 0:
                print("You finished, bot turns starting again...")
            else:
                print("System has concluded, waiting for you.")
        elif self.__states == ["Ended", "Ended"]:
            score = self.sumValues(turn=turn)
            score_1 = self.sumValues(turn=turn_1)
            print("-----------")
            if turn == 0:
                if score > score_1:
                    print(f"You won with {score} against {score_1}.")
                elif score == score_1:
                    print(f"You tied with {score}.")
                else:
                    print(f"You lost with {score} against {score_1}.")
            else:
                if score > score_1:
                    print(f"You lost with {score_1} against {score}.")
                elif score == score_1:
                    print(f"You tied with {score}.")
                else:
                    print(f"You won with {score_1} against {score}.")
            self.__states = ["Ended", "Ended"]
            self.__state = "Ended"
        
    def start(self):
        print("-----------")
        print("Opening packet...")
        self.openPacket()
        time.sleep(2)
        print("Successfully opened the packet!")
        
        turn = 0
        while self.__state != "Ended":
            time.sleep(2)
            if self.__state == "Default":
                self.__state == "Running"
            if self.__states == []:
                for i in range(2):
                    self.__states.append("Running")
            
            if turn == 0:
                turn += 1
            else:
                turn -= 1
            
            if turn == 0:
                self.choiceMenu(turn=turn)            
            time.sleep(3)
            
            
            self.verifyStatement(turn=turn)
            self.play(turn=turn)
        
BlackJack().start()