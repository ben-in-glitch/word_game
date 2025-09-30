#battle_mode v.2
def battle_mode(player, monster):
    print(f'{monster.name}(live:{monster.hp}/damage:{monster.damage}/guard:{monster.defense})')
    while monster.hp >0:
        print(f'{monster.hp}/{monster.maximum_hp}')
        choice = input('attack/run/status:').lower()
        choices = {
            'status': player.check_status,
            'attack': lambda: player.attack(monster),
            'run': player.run
        }
        player.get_basic_skills(monster)
        action = choices.get(choice)
        if action:
            action()
        else:
            print('failed')

        if monster.hp > 0 and not choice == 'status':
            time.sleep(1)
            monster.attack(player)
        if game_over(player):
            return False
    return True
#battle_mode v.1
def battle_mode(player, monster):
    print(f'{monster.name}(live:{monster.hp}/damage:{monster.damage}/guard:{monster.defense})')
    while monster.hp >0:
        choice = input('attack/run/status:').lower()
        if choice == 'status':
            player.check_status()
        elif choice == 'attack':
            player.attack(monster)
        elif choice == 'run':
            player.run()
        elif choice == 'hero magic':
            player.hero_magic(monster)
        elif choice == 'demon king magic':
            player.demon_magic(monster)
        if monster.hp >0 and not choice == 'status':
            time.sleep(1)
            monster.attack(player)
        if game_over(player):
            return False
    return True
# -----
# battle mode v.0
def basic_player_attack(player,Monster,choice):
    if choice == 'run':
        player.run()

    elif choice == 'attack':
        if player.attack() < Monster.basic_guard():
            print(f'{Monster.name} guarded')
            new_damage = player.attack() // 2
            Monster.hp -= new_damage
        else:
            Monster.hp -= player.attack()

        print(f'You attack {Monster.name} ({Monster.hp}/{Monster.maximum_hp})')

def basic_monster_attack(player,Monster):
    print(f'\n{Monster.name} counters')
    time.sleep(1)
    if Monster.attack() < player.basic_guard():
        print('you guarded')
        new_damage = Monster.attack() // 2
        player.hp -= new_damage
    else:
        player.hp -= Monster.attack()

    print(f'{Monster.name} attacks you({player.hp}/{player.maximum_hp})')

def battle_mode_monster(player, Monster):
    print(f'{Monster.name}(live:{Monster.hp}/damage:{Monster.damage}/guard:{Monster.defense})')
    while Monster.hp > 0:
        choice = input(f'\nattack/run/status:').lower()

        if choice == 'status':
            player.check_status()
        else:
            basic_player_attack(player,Monster,choice)
            if Monster.hp > 0:
                basic_monster_attack(player, Monster)
            if game_over(player):
                return False
    return True


def battle_mode_hero(player, Monster):
    print(f'{Monster.name}(live:{Monster.hp}/damage:{Monster.damage}/guard:{Monster.defense})')
    activation = 1
    while Monster.hp >0:
        choice = input('attack/run/status:').lower()
        if choice == 'status':
            player.check_status()
        else:
            if choice == 'hero magic':
                damage = player.hero_magic(0.1)
                Monster.hp -= damage
                print(f'you caused {player.hero_magic_damage} damage')
            else:
                basic_player_attack(player, Monster, choice)

            if Monster.hp > 0:
                if activation % 3 == 0:
                    damage = Monster.hero_magic(0.1)
                    player.hp -= damage
                    print(f'hero magic caused {damage} damage')
                else:
                    basic_monster_attack(player, Monster)
                activation += 1

            if game_over(player):
                return False
    return True

def battle_mode_demon_king(player, Monster):
    print(f'{Monster.name}(live:{Monster.hp}/damage:{Monster.damage}/guard:{Monster.defense})')
    activation = 1
    while Monster.hp >0:
        choice = input('attack/run/status:').lower()
        if choice == 'status':
            player.check_status()
        else:
            if choice == 'hero magic':
                damage = player.hero_magic(0.1)
                Monster.hp -= damage
                print(f'you caused {player.hero_magic_damage} damage')
            else:
                basic_player_attack(player, Monster, choice)

            if Monster.hp > 0:
                if activation % 2 == 0:
                    damage = Monster.demon_king_magic(0.2)
                    player.hp -= damage
                    print(f'demon king magic caused {damage} damage')
                else:
                    basic_monster_attack(player, Monster)

                activation += 1
            if game_over(player):
                return False
    return True
# -------
#hero attack mode
def attack(self, player):
    self.attack_count += 1
    if self.attack_count % 3 == 0:
        print('Hero magic!')
        time.sleep(1)
        chance =0.1
        if random.random() < chance:
            print('\nhero magic! success')
            print(f'hero magic caused {self.hero_magic_damage} damage')
            player.hp -= self.hero_magic_damage
        else:
            print('nothing happened')
    else:
        super().attack(player)

#----------------- items-------------------------
def use_inventory(self,player):
    choice = inquirer.select(
        message="your item:",
        choices= self.inventory +['back'],
        qmark=":>"
    ).execute()

    choices = {
        "equipment" : lambda: Weapon(player).use(player),
        "portions" : lambda: Portion(player).use(player),
        "others" : lambda: print(''),
        "back" : lambda: print('')
    }
    choices.get(choice)()
    if choice  == 'back':
        return
class Weapon(Item):
    def __init__(self, name):
        super().__init__(name)

    def weapons_list(self,player):
        weapons_list = {
            "sword": lambda: self.sword(player),
            "stick": lambda: self.stick(player)
        }
        return weapons_list

    def use(self,player):
        choice = inquirer.select(
            message="your equipment:",
            choices= player.inventory_equipment +['back'],
            qmark=":>"
        ).execute()
        action = self.weapons_list(player).get(choice)
        if action:
            action()
        else:
            print(f"no such weapon")

    def off(self):
        pass

    def weapon(self,weapon_name, damage,player):
        if not player.weapon_equipped:
            player.damage += damage
            print(f'{weapon_name} equipped +{damage} damage')
            player.weapon_equipped =True
        else:
            print(f'weapon is already equipped')

    def sword(self,player):
        self.weapon("sword", 2, player)

    def stick(self,player):
        self.weapon('stick',100, player)

class Portion(Item):
    def __init__(self, name):
        super().__init__(name)

    def portions_list(self,player):
        portions_list = {
            "hp portion" : lambda : self.hp_portion(player),
            "defense portion" : lambda : self.defense_portion(player)
        }
        return portions_list

    def use(self, player):
        choice = inquirer.select(
            message="your portions:",
            choices= player.inventory_portions +['back'],
            qmark=":>"
        ).execute()
        action = self.portions_list(player).get(choice)
        if action:
            action()
            player.inventory_portions.remove(choice)
        else:
            print(f"no such portion")


    def hp_portion(self, player):
        amount = 5
        before = player.hp
        player.hp = min(player.maximum_hp, player.hp + amount)
        print(f"HP healed {player.hp - before} HP")

    def defense_portion(self,player):
        amount = 5
        before = player.defense
        player.defense += amount
        print(f"defense {player.defense - before} defense")

class Item:
    # Item ={}
    def __init__(self,name):
        self.name = name

    def use(self,player):
        raise NotImplementedError

#     @classmethod
#     def register(cls,item_cls):
#         cls.ITEM[item_cls.__name__] = item_cls
#         return item_cls
#
#     @classmethod
#     def create(cls,name):
#         if name in cls.ITEM:
#             return cls.ITEM[name](name)
#         return None
#
# @Item.register
# ------------------------------------------attack
def attack(self, monster):#player
    damage = random.randint(1, self.damage)
    defense = random.randint(1, monster.defense)
    if damage > defense:
        new_damage = damage
        monster.hp -= new_damage
    else:
        new_damage = damage // 2
        monster.hp -= new_damage
        print(f'{monster.name} guarded, damage halved!')
    print(f'you caused {new_damage} damage')

def attack(self,player):#monster
    print(f'\n{self.name} attacks')
    time.sleep(1)
    damage = random.randint(1, self.damage)
    defense = random.randint(1, player.defense)
    if damage > defense:
        new_damage = damage
        player.hp -= new_damage
    else:
        new_damage = damage // 2
        player.hp -= new_damage
        print(f'{player.name} guarded, damage halved!')
    print(f'{self.name} attacks {new_damage} damage')

# ----------------------buff/debuff---------------------------
class Poison(BuffDebuff):
    damage = 0
    end_effect = 0

    def effect(self):
        print('poison effect')

    @classmethod
    def effect_add(cls,receiver,damage, round):
        cls.end_effect = receiver.attack_count +round
        receiver.effect.append(cls)
        cls.damage += damage
        print(f'Poison effect, HP -')


    @classmethod
    def effect_check(cls, receiver):
        if cls in receiver.effect:
            if receiver.attack_count > cls.end_effect:
                receiver.effect.remove(cls)
            else:
                receiver.hp -= cls.damage