````
title: Durak
description: An interactive durak card game between player and computer.
author: Neele Witschenbach
````

# Rules for durak

## for two players:
- six cards for each player
- one additional card is being pulled, the symbol on this card is the triumph 
- the triumph card lies diagonal under the stack
- a triumph card is superior to all, except higher triumphs
- to start the game, the player with the lowest triumph starts attacking (not necessarily
 with this one, since you want to save triumphs for tricky situations)
- to defeat an attack you have to lay any higher card *ontop* of the other
- to push/reverse an attack you have to lay a card with the same value (6,7,8...)
*next* to the other, in this case the defender becomes the attacker
- one can only push if this is the first move, once you defeat one card you can't push another one you've been attacked 
with
- the attacker can add any card with the same value (as long as the stack exist, there can be five attacks, 
if there is no stack anymore the attacker can lay as many cards as the defender has on hand)
- if all cards are beat, they get laid to the side and both players pull cards to have six on hand again, attacker gets
to be first (original triumph card also gets pulled in the end)
- if one cannot beat all cards, they have to take ALL of them and the attacker attacks again,
if one beats all, the defender starts attacking in the next round
- this goes on until one lays their last card, which means they've won

## How to use the code
- lay a card: enter a card in the format (6, Karo) or copy them from the terminal
- push a card: type PUSH, add a blank space and then enter a card in the format described as above
- take the cards: type XXX 
- if you are the defender and have to defeat multiple cards, start the defeat at the last added card 