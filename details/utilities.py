from InquirerPy import inquirer

def basic_prize(player, bonus):
    print('Congratulations')
    prize_pool = ['damage', 'life', 'defense']
    prize = inquirer.select(
        message="please choose your prize:",
        choices= prize_pool,
        qmark=""
    ).execute()

    if prize in prize_pool:
        if prize == 'damage':
            player.buffed_damage += bonus
        elif prize == 'life':
            player.maximum_hp += bonus
        elif prize == 'defense':
            player.buffed_defense += bonus
        print(f'you gained {bonus} {prize}')
    else:
       print('you gained nothing')

def skill_add(player, skill_name, chance, damage):
    print(f'bonus skill - {skill_name}({chance * 100}% causes {damage} damage)')
    player.unlocked_skills.append(skill_name)
    player.unlocked_skills_description[skill_name] = f'{chance * 100}% causes {damage} damage'

def item_add(player, item_name):
    player.inventory.append(item_name)
    print(f'you gained {item_name}')