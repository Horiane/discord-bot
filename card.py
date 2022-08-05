import random
def card():
    global random_card
    global random_card1
    deck="23456789TJQKA"
    random_card=random.choice(deck)
    if random_card=="T" or random_card=="J" or random_card=="K" or random_card=="Q":
        random_card=10
    elif random_card=="A":
        random_card=11
    deck="23456789TJQKA"
    random_card1=random.choice(deck)
    if random_card1=="T" or random_card1=="J" or random_card1=="K" or random_card1=="Q":
        random_card1=10
    elif random_card1=="A":
        random_card1=11