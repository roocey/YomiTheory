#!/usr/bin/python

import sys
import random

if len(sys.argv) > 1:
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)

player_name = raw_input("Welcome! Enter your name: ")
player_name = player_name.capitalize()
print 'Hello, ' + player_name + '. The game is simple: you will be presented with the choice to \'cooperate\' or \'cheat\'. If we both cooperate, we both gain 2 yomi. If one of us cheats, the cheater gains 3 yomi and the other loses 1 yomi. If both of us cheat, neither of us gets any yomi.'
yomi = 0
ai_yomi = 0
choices_list = ['cooperate', 'cheat']
last_choice = -1
cooperate_value = 2
cheat_value = 3
cheat_victim_value = -1
cheat_tie_value = 0
rounds = 0
multiplier = 1
flag = 1
ai_behavior = 0 #0 = matches, 1 = un-matches, 2 = erratic (always flips twice)
ai_trust = 0 #lower = more trusting (if this is 7 or above, the AI will almost always cheat, regardless of behavior | if it's at exactly 0, the AI will cooperate more)
game_state = True

while game_state == True:
    if rounds%12 == 0 and rounds > 0 == 0:
        flag = 2
        multiplier = multiplier * 2
        ai_behavior = random.randint(0, 2)
        behaviors_str = ''
        if '$behaviors' in str(sys.argv):
            if ai_behavior == 0:
                behaviors_str = ' I will match your choices 75% of the time.'
            elif ai_behavior == 1:
                behaviors_str = ' I will un-match your choices 75% of the time.'
            elif ai_behavior == 2:
                behaviors_str = ' I will choose randomly.'
            
        print 'We\'ve played ' + str('{:,}'.format(rounds)) + ' rounds so far. Let\'s up the ante: ' + str('{:,}'.format(multiplier)) + 'x multiplier for all yomi.' + behaviors_str
        
    if rounds%7 == 0 and rounds > 0 == 0:
        flag = 1
        cooperate_value = random.randint(1, 6) * multiplier
        cheat_value = random.randint(1, 5) * multiplier
        cheat_victim_value = random.randint(-1, 1) * multiplier
        cheat_tie_value = random.randint(-2, 1) * multiplier
        if cheat_victim_value < 0 and cheat_tie_value < 0 and random.randint(0, 1) == 0:
            cheat_tie_value = cheat_tie_value * abs(cheat_victim_value)
        if random.randint(0, 1) == 0:
            cooperate_value += cheat_value
        if cheat_tie_value < 0 and random.randint(0, 1):
            cheat_tie_value -= cooperate_value
        if random.randint(0, 3) == 0:
            cheat_victim_value = abs(cheat_victim_value + cheat_value)
        
        last_choice = -1
        rules_change_str = 'We\'ve played ' + str('{:,}'.format(rounds)) + ' rounds so far. Let\'s change the rules: successful cooperation will now be worth ' + str('{:,}'.format(cooperate_value)) + ' yomi.'
        if cheat_victim_value <= 0:
            rules_change_str += ' Successful cheating will be worth ' + str('{:,}'.format(cheat_value)) + ' yomi and cost the victim ' + str('{:,}'.format(abs(cheat_victim_value))) + ' yomi.'
        else:
            rules_change_str += ' Successful cheating will be worth ' + str('{:,}'.format(cheat_value)) + ' yomi, but the victim will earn ' + str('{:,}'.format(cheat_victim_value)) + ' yomi.'
        if cheat_tie_value == 0:
            rules_change_str += ' Mutual cheating will cost no yomi.'
        elif cheat_tie_value > 0:
            rules_change_str += ' Mutual cheating will earn us both ' + str('{:,}'.format(cheat_tie_value)) + ' yomi.'
        elif cheat_tie_value < 0:
            rules_change_str += ' Mutual cheating will cost us both ' + str('{:,}'.format(abs(cheat_tie_value))) + ' yomi.'
        print rules_change_str

        
    choice = None
    while choice == None:
        choice = raw_input('Decide: \'cooperate\' or \'cheat\'? ')
        choice = choice.lower()
        flip = random.randint(0, 1) #flip a coin to decide the AI's choice (0 = cooperate, 1 = cheat)
        if ai_behavior == 0:
            if last_choice == 0 and flip == 1:
                flip = random.randint(0, 1) #reroll to try and match player
            elif last_choice == 1 and flip == 0:
                flip = random.randint(0, 1)
        elif ai_behavior == 1:
            if last_choice == 0 and flip == 0:
                flip = random.randint(0, 1)
            elif last_choice == 1 and flip == 1:
                flip = random.randint(0, 1)
        elif ai_behavior == 2:
            flip = random.randint(0, 1)

        if ai_trust >= random.randint(1, 7) and flip == 0: #cheat cheating players more often, despite behavioral tendencies
            flip = random.random_int(0, 1)
            if ai_trust >= 7 and flip == 0: #cheat REALLY cheating players VERY often
                flip = random.random_int(0, 1)
        if ai_trust == 0 and random.randint(0, 1) == 0 and flip == 1: #cooperate with cooperative players more often, despite behavioral tendencies
            flip = random.randint(0, 1)
            if flip == 0 and ai_trust == 0 and random.randint(0, 10) == 0: #1-in-11 chance to catch "suckers" (overly cooperative players)
                ai_trust = 7

        if choice in choices_list:
            rounds += 1
            if choice == 'cooperate':
                last_choice = 0
                ai_trust -= 2
                if flip == 0:
                    yomi += cooperate_value*flag
                    ai_yomi += cooperate_value*flag
                    print 'We both cooperated. We both earned ' + str('{:,}'.format(cooperate_value*flag)) + ' yomi!'
                else:
                    yomi += cheat_victim_value*flag
                    ai_yomi += cheat_value*flag
                    if cheat_victim_value <= 0:
                        print 'You cooperated, but I cheated! I earned ' + str('{:,}'.format(cheat_value*flag)) + ' yomi and you lost ' + str('{:,}'.format(abs(cheat_victim_value*flag))) + ' yomi.'
                    else:
                        print 'You cooperated, but I cheated! I earned ' + str('{:,}'.format(cheat_value*flag)) + ' yomi and you earned ' + str('{:,}'.format(cheat_victim_value*flag)) + ' yomi.'
            else:
                last_choice = 1
                ai_trust += 1
                if flip == 0:
                    yomi += cheat_value*flag
                    ai_yomi += cheat_victim_value*flag
                    if cheat_victim_value <= 0:
                        print 'You cheated, but I cooperated. You earned ' + str('{:,}'.format(cheat_value*flag)) + ' yomi and I lost ' + str('{:,}'.format(abs(cheat_victim_value*flag))) + ' yomi.'
                    else:
                        print 'You cheated, but I cooperated. You earned ' + str('{:,}'.format(cheat_value*flag)) + ' yomi and I earned ' + str('{:,}'.format(cheat_victim_value*flag)) + ' yomi.'
                else:
                    yomi += cheat_tie_value*flag
                    ai_yomi += cheat_tie_value*flag
                    if cheat_tie_value == 0:
                        print 'We both cheated. Our yomi remains unchanged...'
                    elif cheat_tie_value < 0:
                        print 'We both cheated. We both lost ' + str('{:,}'.format(abs(cheat_tie_value*flag))) + ' yomi...'
                    elif cheat_tie_value > 0:
                        print 'We both cheated. We both earned ' + str('{:,}'.format(cheat_tie_value*flag)) + ' yomi!'

            if yomi < 0:
                yomi = 0
            if ai_yomi < 0:
                ai_yomi = 0
            if ai_trust < 0:
                ai_trust = 0
            if ai_trust > 7:
                ai_trust = 7
            print 'Round #' + str('{:,}'.format(rounds)) + ': You have ' + str('{:,}'.format(yomi)) + ' yomi. I have ' + str('{:,}'.format(ai_yomi)) + ' yomi.'
        else:
            print choice.capitalize() + ' is not a valid choice.'
            choice = None
else:
    print 'Uh oh...'
    
