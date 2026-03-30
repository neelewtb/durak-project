"""
Regeln fuer Durak:
Jeder Spieler hat 6 Karten, nach dem Austeilen wird noch eine Karte aus dem Stapel gezogen und offen im 90Grad Winkel
unter den verbleibenden Haufen gelegt. Das Zeichen auf der offenen Karte ist der Trumpf: eine Karte mit z.B. Herz ist
nun maechtiger als alle anderen, ausser hoehere Herz-Karten. Um das Spiel zu starten beginnt derjenige, der den
niedrigsten Trumpf hat, wobei es sinnvoll ist nicht direkt diese Karte zu benutzen (Truempfe für zwickliche Situationen
aufbewahren). Spieler A greift nun Spieler B an. Spieler B muss sich verteidigen indem er 1. die Karte schlägt und eine
hoehere Karte AUF die gegnerische legt, oder 2. eine Karte desselben Zeichens (6,7,8....,As) hat und DANEBEN legt.
In diesem Fall geht der Angriff auf den ursprünglichen Angreifer zurück und er hat dieselben Optionen. Sollte man
weder schlagen noch den Angriff weiterleiten können, muss man ALLE vorliegenden Karten aufnehmen und man wird danach
wieder angegriffen. In dem Fall, dass man schlägt kann der Angreifende weitere Karten legen, aber nur von dem Zeichen
die vor ihm liegen. Bsp: Angriff mit 7 Pik, geschlagen mit 9 Pik (übereinander), dann 9 Karo NEBEN den ersten Haufen,
geshlagen mit Bube Karo, neuer Haufen mit Bube Kreuz usw. Wenn der Angegriffende alle Karten geschlagen hat, und der
Angreifende keine mehr legen kann (oder will, strategisch manchmal schlauer) werden die Karten beiseite gelegt und
alle Spieler ziehen auf 6 Karten wieder auf. Solange der Nachziehstapel noch da ist, darf man nur mit 5 Karten
angreifen, danach mit sovielen wie der Anzugreifende auf der Hand hat. Die Trumpf-Karte unter dem Stapel wird auch mit-
gezogen. Angreifer zieht zuerst. Gewonnen hat der, der zuerst alle Karten los ist.

"""

import ast
import random

#Rahmenbedingungen festlegen, Zeichen, Symbole, Hierachie der KArten
suits = ['Herz', 'Karo','Pik','Kreuz']
cards = ['6', '7', '8','9','10','B','D','K','A']
cards_order = {'6':0, '7':1, '8':2, '9':3, '10':4,
               'B':5, 'D':6, 'K':7, 'A':8}

def exec_game():
    prio = [(card, suit) for suit in suits for card in cards]
    #Verteilung der Karten und bestimmen was das Trumpfsymbol ist
    random.shuffle(prio)
    player_cards = prio[:6]
    computer_cards = prio[6:12]
    staple = prio[12:]
    triumph = prio[-1]
    triumph_suit = triumph[1]

    print("Trumpf ist:", triumph_suit)

    def sortedcards(hand):
        return sorted(hand, key=lambda card: cards_order[card[0]])

    player_cards = sortedcards(player_cards)
    computer_cards = sortedcards(computer_cards)

    def lowest_triumph(hand):
        trumps = [c for c in hand if c[1] == triumph_suit]
        if not trumps:
            return None
        return min(trumps, key=lambda c: cards_order[c[0]])

    # Beginner bestimmen -> derjenige mit tiefsten Trumpf
    p_low = lowest_triumph(player_cards)
    c_low = lowest_triumph(computer_cards)

    if p_low and c_low:
        attacker = "Spieler" if cards_order[p_low[0]] < cards_order[c_low[0]] else "Computer"
    elif p_low:
        attacker = "Spieler"
    elif c_low:
        attacker = "Computer"
    else:
        attacker = random.choice(["Spieler","Computer"])

    defender = "Computer" if attacker == "Spieler" else "Spieler"

    print("Start:", attacker)

    #Aktives Spiel ab hier

    while player_cards and computer_cards:

        table = []
        round_over = False

        #erste Angriffskarte bestimmen
        if attacker == "Spieler":
            print("Deine Karten:", player_cards)
            atk = ast.literal_eval(input("Angriffskarte: "))
            player_cards.remove(atk)
        else:
            non_trump = [c for c in computer_cards if c[1] != triumph_suit]
            atk = non_trump[0] if non_trump else computer_cards[0]
            computer_cards.remove(atk)
            print("Computer greift an mit:", atk)

        table.append((atk, None))

        # while-Schleife zum simulieren einer Runde
        while not round_over:

            # defender reagiert auf alle Angriffee
            for i, (attack, defense) in enumerate(table):

                if defense is not None:
                    continue

                # player ist defender
                if defender == "Spieler":
                    print("Tisch:", table)
                    print("Deine Karten:", player_cards)

                    move = input("Karte spielen, PUSH (Zeichen,Symbol) oder XXX: ")

                    #aufnehmen -> alle Karten zur Hand hinzufügen
                    if move == "XXX":
                        cards_on_table = [c for p in table for c in p if c]
                        player_cards.extend(cards_on_table)
                        round_over = True
                        break

                    # schieben wenn gleiches Zeichen vorhanden
                    elif move.startswith("PUSH"):
                        try:
                            push_card = ast.literal_eval(move[5:])

                            if push_card in player_cards and push_card[0] == attack[0]:
                                player_cards.remove(push_card)

                                print("Du schiebst mit:", push_card)

                                table.append((push_card, None))

                                # Rollen wechseln
                                attacker, defender = defender, attacker

                                continue
                            else:
                                print("Ungültiger Push!")
                                continue

                        except:
                            print("Format falsch!")
                            continue

                    # wenn schieben nicht möglich-> normales schlagen
                    else:
                        try:
                            move = ast.literal_eval(move)

                            valid = False
                            if move[1] == attack[1] and cards_order[move[0]] > cards_order[attack[0]]:
                                valid = True
                            if move[1] == triumph_suit and attack[1] != triumph_suit:
                                valid = True

                            if valid:
                                player_cards.remove(move)
                                table[i] = (attack, move)
                            else:
                                print("Ungültig → nimm Karten")
                                cards_on_table = [c for p in table for c in p if c]
                                player_cards.extend(cards_on_table)
                                round_over = True
                                break

                        except:
                            print("Ungültige Eingabe")
                            continue

                # Computer ist defender
                else:
                    # schieben ist Priorität für den Computer
                    if len(player_cards) > 1:
                        push_cards = [c for c in computer_cards if c[0] == attack[0]]

                    if push_cards:
                        card = push_cards[0]
                        computer_cards.remove(card)

                        print("Computer schiebt mit:", card)

                        table.append((card, None))  # Karte hinzufuegen

                        # Rollen wechseln
                        attacker, defender = defender, attacker

                        continue
                    # gleiche Farbe schlagen
                    same = [c for c in computer_cards if c[1] == attack[1] and cards_order[c[0]] > cards_order[attack[0]]]

                    if same:
                        card = min(same, key=lambda c: cards_order[c[0]])
                        computer_cards.remove(card)
                        table[i] = (attack, card)
                        print("Computer verteidigt mit:", card)
                    else:
                        # mit Trumpf schlagen
                        trumps = [c for c in computer_cards if c[1] == triumph_suit]
                        #hier wollte ich simulieren, dass auch wenn man manchmal mit einem Trumpf schlagen koennte,
                        #es vom Spielverlauf manchmal schlauer ist es zu lassen (z.B viele nuetzlche hohe Karten liegen vor,
                        #Trumpf extrem hoch,..)
                        if trumps and random.random() < 0.45:
                            card = min(trumps, key=lambda c: cards_order[c[0]])
                            computer_cards.remove(card)
                            table[i] = (attack, card)
                            print("Computer verteidigt mit Trumpf:", card)
                        else:
                            print("Computer nimmt Karten")
                            cards_on_table = [c for p in table for c in p if c]
                            computer_cards.extend(cards_on_table)
                            round_over = True
                            break

            if round_over:
                break

            # pruefen ob alle Angriffkarten geschlagen worden sind
            if all(d is not None for _, d in table):
                print("Alles geschlagen")

                # Option einwerfen hinzufuegen
                values_on_table = [card[0] for pair in table for card in pair if card]

                if attacker == "Computer":
                    possible = [c for c in computer_cards if c[0] in values_on_table]
                    if possible:
                        new_card = possible[0]
                        computer_cards.remove(new_card)
                        table.append((new_card, None))
                        print("Computer wirft ein:", new_card)

                        continue

                    else:
                        round_over = True

                else:
                    print("Tisch:", table)
                    print("Deine Karten:", player_cards)

                    move = input("Einwerfen oder ENTER: ")

                    if move != "":
                        move = ast.literal_eval(move)

                        if move in player_cards and move[0] in values_on_table:
                            player_cards.remove(move)
                            table.append((move, None))
                            print("Du wirfst ein:", move)

                            continue

                    # nichts eingeworfen → Runde Ende
                    round_over = True
                # Angriff und Verteidigung wechseln
                attacker, defender = defender, attacker

        # Nachziehen implementieren
        def draw(hand):
            while len(hand) < 6 and staple:
                hand.append(staple.pop())

        if attacker == "Spieler":
            draw(player_cards)
            draw(computer_cards)
        else:
            draw(computer_cards)
            draw(player_cards)

        player_cards = sortedcards(player_cards)
        computer_cards = sortedcards(computer_cards)

        print("♠ ♣ ♥ ♦neue Runde ♠ ♣ ♥ ♦")

    # wenn einer keine Karten mehr hat-> Sieg
    if not player_cards:
        print("꧁Du hast gewonnen!꧂")
    else:
        print("☹Computer hat gewonnen! ☹")









