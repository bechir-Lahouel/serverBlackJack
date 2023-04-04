#!/usr/bin/env python3
from datetime import datetime
import asyncio
import random

#couleur des cartes
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

s = ['♠', '♥', '♣', '♦']
f = ['king', 'Queen', 'Jack', 'Ace', 'ten', 'nine', 'eight', 'seven', 'six', 'five', 'four', 'three', 'two']
v = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'Jack': 10, 'Queen': 10, 'king': 10, 'Ace': 11}

cadrTemplate = [ '╔══════╗',
                 '║ {:<2}   ║',
                 '║      ║',
                 '║   {:<2} ║',
                 '╚══════╝']
def drawCard(index, suit, value):
    if suit == '♥' or suit == '♦':
        color = FAIL
    else:
        color = OKBLUE

    if index == 1:
        return color + cadrTemplate[index].format( suit ) + ENDC
    elif index == 3:
        return color + cadrTemplate[index].format( value ) + ENDC
    else:
        return color + cadrTemplate[index] + ENDC

blackJack = WARNING + " /$$$$$$$ /$$       /$$$$$$   /$$$$$$ /$$   /$$    /$$$$$  /$$$$$$   /$$$$$$ /$$   /$$  \n" \
            "| $$  \ $| $$     | $$  \ $$| $$  \__| $$ /$$/       | $$| $$  \ $$| $$  \__| $$  /$$/  \n" \
            "| $$  \ $| $$     | $$  \ $$| $$  \__| $$ /$$/       | $$| $$  \ $$| $$  \__| $$ /$$/   \n" \
            "| $$$$$$$| $$     | $$$$$$$$| $$     | $$$$$/        | $$| $$$$$$$$| $$     | $$$$$/    \n" \
            "| $$__  $| $$     | $$__  $$| $$     | $$  $$   /$$  | $$| $$__  $$| $$     | $$  $$    \n" \
            "| $$  \ $| $$     | $$  | $$| $$    $| $$\  $$ | $$  | $$| $$  | $$| $$    $| $$\  $$   \n" \
            "| $$$$$$$| $$$$$$$| $$  | $$|  $$$$$$| $$ \  $$|  $$$$$$/| $$  | $$|  $$$$$$| $$ \  $$  \n" \
            "|_______/|________|__/  |__/ \______/|__/  \__/ \______/ |__/  |__/\______/ |__/  \__/  "+ENDC+"\n"

youWin =    OKGREEN + "|   __   __                    _        _  \n" \
                      "|   \ \ / /___  _  _  __ __ __(_) _ _  | | \n" \
                      "|    \ V // _ \| || | \ V  V /| || ' \ |_| \n" \
                      "|     |_| \___/ \_,_|  \_/\_/ |_||_||_|(_) "+ENDC+"\n"

DelearWin =    FAIL   + "|  __   __            _                  | \n" \
                        "|  \ \ / /___  _  _  | |    ___   ____   | \n" \
                        "|   \ V // _ \| || | | |__ / _ \ (  (    | \n" \
                        "|    |_| \___/ \_,_| |____|\___/  )___)  | "+ENDC+"\n"


dealerTitle = OKCYAN + "/)/)/)/)/)/)/)/)/)  | \|_ |_||  |_ |_)  /)/)/)/)/)/)/)/)/) \n" \
         "(/(/(/(/(/(/(/(/(/  |_/|__| ||__|__| \  (/(/(/(/(/(/(/(/(/ "+ENDC+"\n"

playerTile = OKBLUE + "                     _     _     __ _                     \n" \
                      "/)/)/)/)/)/)/)/)/)  |_)|  |_|\/ |_ |_)  /)/)/)/)/)/)/)/)/)\n" \
                      "(/(/(/(/(/(/(/(/(/  |  |__| | | |__| \  (/(/(/(/(/(/(/(/(/"+ENDC+"\n"


class Hand():
    def __init__(self,name, writer = None, reader = None):
        self.name = name
        self.writer = writer
        self.reader = reader
        self.Stand = False
        self.cards = [] #cards is tuple of (suit,face)
        self.value = 0
        self.event = asyncio.Event()

    def add_card(self,card):
        self.cards.append(card)
        self.adjust_for_ace()

    def adjust_for_ace(self):
        nbAce = 0
        self.value = 0
        for c in self.cards:
            if c[1] == 'Ace':
                nbAce += 1
            else:
                self.value += v[c[1]]

        for i in range(nbAce):
            if self.value + 11 > 21:
                self.value += 1
            else:
                self.value += 11

    def __str__(self):
        lisCadre = ""
        for i in range(len(cadrTemplate)):
            for c in self.cards:
                lisCadre += drawCard(i, c[0], str(v[c[1]])) + "  "
            lisCadre += "\n"

        if self.value > 21:
            lisCadre += f" value : {FAIL}{self.value}{ENDC}\n"
        else:
            lisCadre += f" value : {OKGREEN}{self.value}{ENDC}\n"
        return lisCadre

class blackjackTable:
    def __init__(self,name, time):
        self.deck = [ (suit, card ) for card in f for suit in s]
        random.shuffle(self.deck)
        self.dealer = Hand(name="dealer")
        self.name = name
        self.time = time
        self.startgame = False
        self.startingTime = None
        self.endGame = False
        self.players = []

    def hit(self,player):
        player.add_card(self.deck.pop())

    def hitDealer(self):
        self.dealer.add_card(self.deck.pop())

    def addPlayer(self, player):
        if self.players.__len__() == 0 :
            self.startingTime = datetime.now()
            self.hitDealer()
        self.players.append(player)



listTables = []

async def playGame(CourenTable,player_):
    while True :
        player_.writer.write(".\n".encode())
        await player_.writer.drain()
        data = await player_.reader.readline()
        srt = data.decode().split(' ')
        if srt[0] == 'MORE':
            srt = srt[1].strip()
            if srt == '1':
                CourenTable.hit(player_)
                player_.writer.write(str(player_).encode())
                await player_.writer.drain()
            else:
                player_.Stand = True
                return


async def hundeljoueur(r,w):
    global listTables
    client,_ = w.get_extra_info(name='peername')
    print("joueur {} est conneté!".format(client));

    w.write(f'{HEADER} welcome {client} to blackjack game {ENDC}\n'.encode())

    name = await r.readline()
    srt = name.decode().split(' ')
    if srt[0] == 'NAME':
        name = srt[1].strip() # remove the new line character

    #check if table exist
    CourenTable = None
    for table in listTables:
        if table.name == name:
                CourenTable = table
                break

    if CourenTable == None or CourenTable.startgame == True:
        if CourenTable == None :
            w.write(f"error : {FAIL} le table can't be found {ENDC}\n".encode())
        else:
            w.write(f"error : {FAIL} the game is already started {ENDC}\n".encode())
        w.write("END\n".encode())
        w.close()
        return

    #add player to table
    player_ = Hand(name = client, writer=w,  reader=r)
    CourenTable.addPlayer(player_)
    w.write(f"{OKGREEN}welcome to \"{CourenTable.name}\"{ENDC}\n".encode())

    tempsReste = CourenTable.time - (datetime.now() - CourenTable.startingTime).seconds
    while tempsReste > 0:
        w.write(f"{OKBLUE}le jeux commence dans {tempsReste} secondes {ENDC}\n".encode())
        await w.drain()
        if tempsReste > 5 and tempsReste % 5 == 0:
            await asyncio.sleep(5)
        else:
            await asyncio.sleep(1)
        tempsReste = CourenTable.time - (datetime.now() - CourenTable.startingTime).seconds

    CourenTable.startgame = True

    #add 2 card to player
    for i in range(2):
        CourenTable.hit(player_)

    clear = "\n" * 100
    w.write(clear.encode())
    w.write(blackJack.encode())
    w.write("\n".encode())
    #show the cards
    w.write(dealerTitle.encode())
    #show card to player
    w.write(str(CourenTable.dealer).encode())
    w.write(playerTile.encode())
    player_.writer.write(str(player_).encode())


    await asyncio.gather(playGame(CourenTable,player_))


    for player in CourenTable.players :
        if player.Stand == False:
            await player_.event.wait()
            break

    for player in CourenTable.players :
        player.event.set()

    #if dealer n
    if CourenTable.endGame == False:
        CourenTable.endGame = True
        while CourenTable.dealer.value < 17:
            CourenTable.hitDealer()
        listTables.remove(CourenTable)

    #if player is over 21
    if player_.value > 21 :
        w.write(DelearWin.encode())
        w.write("END\n".encode())
        w.close()

    w.write(dealerTitle.encode())
    w.write(str(CourenTable.dealer).encode())
    w.write(playerTile.encode())
    player_.writer.write(str(player_).encode())
    if CourenTable.dealer.value > 21 or CourenTable.dealer.value < player_.value:
        w.write(youWin.encode())
    elif CourenTable.dealer.value > player_.value :
        w.write(DelearWin.encode())
    else:
        w.write("DRAW \n".encode())

    w.write("END\n".encode())
    w.close()






async def hundelCroupier(r,w):
    w.write( f"{OKGREEN}welcome to blackjack game {ENDC}\n".encode())
    data = await r.readline()
    srt = data.decode().split(' ')
    if srt[0] == 'NAME':
        table = srt[1].strip()
    else:
        w.write("error : missing name\n".encode())
        w.close()
        return

    w.write(" \n".encode())
    data = await r.readline()
    srt = data.decode().split(' ')
    if srt[0] == 'TIME':
        time = srt[1].strip()
    listTables.append( blackjackTable(name = table, time = int(time)))
    w.write(f"{OKGREEN} {table} {OKBLUE}was created successfully {ENDC}\n".encode())
    w.close()


async def main():
    serverC = await asyncio.start_server(client_connected_cb=hundelCroupier, port=668)
    serverj = await asyncio.start_server(client_connected_cb=hundeljoueur, port=667)
    await asyncio.gather(serverC.serve_forever(), serverj.serve_forever())

if __name__ == '__main__':
    asyncio.run(main())
