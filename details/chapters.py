import random, utilities, characters, time
from battle import battle_mode
from InquirerPy import inquirer


def intro():
    print('Welcome, traveller')
    name = input('Tell me your name: ').lower().capitalize()
    job = input('Choose your job(warrior/mage/archer): ').lower().capitalize()
    print('let us begin your journey...')
    job_map ={"Warrior": characters.Warrior,
              "Mage": characters.Mage,
              "Archer": characters.Archer}
    job_class = job_map.get(job, characters.Traveller)
    return job_class(name)

def chapter1(player):
    print('Chapter 1:The cave')
    monster = characters.Monster('goblin', 7, 7, 2, 1)

    game = battle_mode(player,monster)
    if game:
        bonus = random.randint(1, 3)
        utilities.basic_prize(player, bonus)

def chapter2(player):
    print('Chapter 2:The Forrest')
    print('You ate a mysterious mushroom, live recovered')
    player.hp = player.maximum_hp
    monster = characters.Witch('witch', 10, 10, 3, 2)

    game = battle_mode(player,monster)
    if game:
        bonus = random.randint(1, 3)
        utilities.basic_prize(player, bonus)

def chapter3(player):
    print('Chapter 3:The Town')
    print('You ate a mysterious mushroom, live recovered')
    print('Hero: Welcome traveller')
    player.hp = player.maximum_hp

    monster = characters.Hero('Hero', 18, 18, 4, 3)
    game = battle_mode(player,monster)
    if game:
        bonus = random.randint(1, 3)
        utilities.basic_prize(player, bonus)
        utilities.skill_add(player, 'hero magic', 0.1, 10)
    else:
        print('hero :You are not strong enough')

def chapter4(player):
    print('Chapter 4:The Castle')
    print('You ate a mysterious mushroom, live recovered')
    player.hp = player.maximum_hp
    print('Demon King: You must be the new hero')
    monster = characters.DemonKing('Demon king', 35, 35, 5, 4)
    game =battle_mode(player,monster)
    if game:
        bonus = random.randint(1, 100)
        utilities.basic_prize(player, bonus)
        utilities.skill_add(player, 'demon magic', 0.5, 20)
    else:
        print('demon king :See you next life, young traveller')

def chapter5(player):
    print('Chapter 5:Nothing Here')
    print('You ate a mysterious mushroom, live recovered')
    player.hp = player.maximum_hp
    monster = characters.Monster('Kiwi bird', 50, 50, 1, 1)
    game  = battle_mode(player,monster)
    if game:
        bonus = random.randint(1, 100)
        utilities.basic_prize(player, bonus)
        utilities.item_add(player, 'PortionSuper')

def hidden_chapter_wind_city(player):
    if random.random() < 0.2:
        print('you entered the city of wind')
        time.sleep(1)
        choice = inquirer.select(
            message = 'choose one NPC :>',
            choices = ["Great Magician Sophie","Hunter Joe", "Champion Zac", "Ruler Benny"]
        ).execute()

        choices = {
            "Great Magician Sophie" : lambda:great_magician_sophie(player),
            "Hunter Joe" : lambda : hunter_joe(player),
            "Champion Zac": lambda : champion_zac(player),
            "Ruler Benny" : lambda : ruler_benny(player),
        }
        choices.get(choice)()

def great_magician_sophie(player):
    print(f'Hidden Chapter ---- Great Magician Sophie')
    print(f'hello {player.name}')
    print('I believe this is helpful to your Journey')
    time.sleep(1)
    utilities.item_add(player, "PortionHpMax")

def hunter_joe(player):
    print(f'Hidden Chapter ---- Hunter Joe')
    print('hello, Traveller')
    print(f"I found this 'SuperStick'.")
    time.sleep(1)
    utilities.item_add(player, "SuperStick")

def champion_zac(player):
    print(f'Hidden Chapter ---- Champion Zac')
    print('hello, my friend')
    print('This is the secret to win every battle')
    time.sleep(1)
    utilities.item_add(player, "PortionSuper")

def ruler_benny(player):
    print(f'Hidden Chapter ----Ruler Benny')
    print('you make the right choice')
    print('let me give you a bit of luck')
    time.sleep(1)
    player.damage = max(0,random.choice([0,100]))
    print(f'your damage is now {player.damage}')

all_chapters = [chapter1,chapter2,chapter3,chapter4,chapter5]

chapters_transform = {
    chapter1 : "chapter1",
    chapter2 : "chapter2",
    chapter3 : "chapter3",
    chapter4 : "chapter4",
    chapter5 : "chapter5"
}

