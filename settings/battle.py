import time
from settings import characters
from InquirerPy import inquirer

def game_over(player):
    return player.hp <= 0

def attack_exception(player,choice):
    return choice in player.other_options

def battle_mode(player, monster):
    player.attack_count = 0
    monster.attack_count = 0
    while monster.hp >0 and player.hp > 0:
        print(f'{monster.name}(HP:{monster.hp}/{monster.maximum_hp},damage:{monster.damage + monster.buffed_damage},guard:{monster.defense + monster.buffed_defense})')
        choice = inquirer.select(
            message="decide your action:",
            choices= characters.show_all_skills(player),
            qmark =":>"
        ).execute()

        print('')
        skill_action = characters.available_skills(player, monster).get(choice)
        skill_action()

        if not attack_exception(player,choice):
            characters.check_buff(player)
            characters.check_debuff(player)
            player.attack_count += 1

        if game_over(player):
            return False

        print('')
        if monster.hp > 0 and not attack_exception(player, choice):
            monster.attack_count += 1
            time.sleep(1)
            print(f'{monster.name} attacks')
            time.sleep(1)
            monster.attack(monster, player)
            print(f'{player.name}:{player.hp}/{player.maximum_hp}\n')


        if game_over(player):
            return False


    print(f'{monster.name} was defeated.')
    return True

