import json
import os
import time
import random

class Hangman:
    __letters: list[str]
    __tries: list[str]
    __damage: int
    __board: str
    __theme: str
    __themes: dict[str, list[str]]
    __running: bool
    __icons: dict[str, str]
    __icons_list: list[str]
    __word: str
    __words: list[str]
    __current: str
    __result: str
    __lang: str
    __langs: list[str]
    __langs_formatted: list[str]
    __texts: dict[str, dict[str, str]]
    __responses: dict[str, list[str]]
    
    def __init__(self):
        self.__letters = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        ]
        self.__tries = []
        self.__damage = 0
        self.__theme = None
        self.__themes = {
            "en": ["animals", "colors", "countries", "fruits", "veggies"],
            "fr": ["animaux", "couleurs", "pays", "fruits", "legumes"],
            "es": ["animales", "colores", "pais", "verduras", "legumbres"]
        }
        self.__running = False
        self.__board = None
        self.__lang = "en"
        self.__langs = ["en", "fr", "es"]
        self.__langs_formatted = ["🇬🇧 (en)", "🇫🇷 (fr)", "🇪🇸 (es)"]
        
        self.__texts = {
            "en": {
                "theme": "Choose a category from the list above:",
                "preparation": "Lemme 3 seconds to prepare everything!",
                "letter": "Choose any letter.",
                "lost": "Lost",
                "win": "Win",
                "intro": "Choose a letter and try your best!",
                "red": "Red letters = used",
                "green": "Green letters = waiting for you!",
                "conclu": "Game has conclude, thanks for playing.",
                "replay": "Do you want to play an another game?"
            },
            "fr": {
                "theme": "Choisis une catégorie de la liste du dessus:",
                "preparation": "Laisse moi 3 secondes pour préparer le tout!",
                "letter": "Choisis une lettre.",
                "lost": "Perdu",
                "win": "Victoire",
                "intro": "Choisis une lettre et fais de ton mieux!",
                "red": "Lettres rouges = utilisées",
                "green": "Lettres vertes = N'attendes que toi!",
                "conclu": "La partie s'est finie, merci d'y avoir joué.",
                "replay": "Veux tu rejouer une partie ?"
            },
            "es": {
                "theme": "Elige una categoría de la lista de arriba:",
                "preparation": "Dame 3 segundos para preparar todo!",
                "letter": "Elige cualquier letra.",
                "lost": "Perdido",
                "win": "Ganar",
                "intro": "Elige una letra y haz tu mejor esfuerzo!",
                "red": "Letras rojas = usadas",
                "green": "Letras verdes = esperando por ti!",
                "conclu": "El juego ha concluido, gracias por jugar.",
                "replay": "¿Te quieras juegar un nuevo partida?"
            }

        }
        
        self.__responses = {
            "en": ["yes", "no"],
            "fr": ["oui", "non"],
            "es": ["si", "no"]
        }
        
        self.__icons = {
            "hat": "🎩",
            "head": "😟",
            "shirt": "👕",
            "pants": "🩳",
            "boots": "👞👞"
        }
        self.__icons_list = ["hat", "head", "shirt", "pants", "boots"]
        self.__words = []
        self.__word = ""
        self.__current = ""
        self.__result = "Undefined"
        
    def openFile(self) -> None:
        with open(f"./json/{self.__lang}/{self.__theme}.json", "r") as file:
            self.__words = json.load(file)
    
    def askTheme(self) -> str:
        theme = None
        while not theme or not theme.lower() in self.__themes[self.__lang]:
            os.system("cls")
            print(self.__themes[self.__lang])
            theme = input(f"{self.__texts[self.__lang]["theme"]}\n")
        os.system("cls")
        return theme
    
    def askReplay(self) -> str:
        response = None
        while not response or not response.lower() in self.__responses[self.__lang]:
            os.system("cls")
            self.showGame(True)
            print("----------------------------------------------------")
            print(self.__responses[self.__lang])
            response = input(f"{self.__texts[self.__lang]["replay"]}\n")
            
        os.system("cls")
        if self.__responses[self.__lang][0] == response:
            Hangman().start()
        else:
            self.__running = False
    
    def askLang(self) -> str:
        lang = None
        while not lang or not lang.lower() in self.__langs:
            os.system("cls")
            print(self.__langs_formatted)
            lang = input("Choose a lang from the list above:\n")
        os.system("cls")
        return lang
    
    def showState(self) -> bool:
        return self.__running
    
    def showBoard(self) -> str:
        self.__board = "\n|‾‾‾‾‾‾‾| \n|      "
        for i in range(5):
            self.__board += self.__icons[self.__icons_list[i]] if self.__damage > i else ' '
            self.__board += ' \n|      '
        self.__board += '\n|__________                      \n'
        self.__board += self.__current
    
        return self.__board

    
    def showGame(self, end_statement: bool) -> None:
        if end_statement == False:
            print(f"\033[44m{self.__texts[self.__lang]["intro"]}\033[0m")
            print(f"\033[41m{self.__texts[self.__lang]["red"]}\033[0m")
            print(f"\033[42m{self.__texts[self.__lang]["green"]}\033[0m")
        else:
            print(f"\033[44m{self.__texts[self.__lang]["conclu"]}\033[0m")
            print(f"\033[4{str(1) if self.__result == f"{self.__texts[self.__lang]["lost"]} :/" else str(2)}m{self.__result}\033[0m")
        print(self.showBoard())
        for letter in self.__letters:
            print(f"\033[42m {letter} \033[0m", end=" ") if not letter in self.__tries else print(f"\033[41m {letter} \033[0m", end=" ")
        print()
    
    def round(self) -> None:
        os.system("cls")
        letter = None
        while not letter in self.__letters or letter in self.__tries:
            os.system("cls")
            self.showGame(False)
            print("----------------------------------------------------")
            letter = input(f"{self.__texts[self.__lang]["letter"]}\n")
        
        self.__tries.append(letter.lower())
    
        
        if not letter.lower() in self.__word:
            self.__damage += 1
            if self.__damage >= 5:
                self.__result = f"{self.__texts[self.__lang]["lost"]} :/"
                self.__current = self.__word
                os.system("cls")
                self.showGame(True)
            
        else:
            current = list(self.__current)
            for i, char in enumerate(self.__word):
                if char == letter.lower():
                    current[i] = char
            self.__current = "".join(current)

            
        if self.__current == self.__word:
            self.__result = f"{self.__texts[self.__lang]["win"]} :)"
            self.__current = self.__word
            os.system("cls")
            self.showGame(True)
            self.askReplay()
    
    def start(self) -> None:
        os.system("cls")
        self.__lang = self.askLang()
        self.__theme = self.askTheme()
        print(self.__texts[self.__lang]["preparation"])
        self.openFile()
        time.sleep(3)
        os.system("cls")
        self.__running = True
        self.__word = self.__words[random.randint(0, len(self.__words)-1)]
        word = list(self.__word)
        for i in range(len(word)):
            self.__current += "?" if word[i] != " " else " "
        while self.showState():
            if not self.__word:
                self.__running = False
                break
            
            self.round()

Hangman().start()
