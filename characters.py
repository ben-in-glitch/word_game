import random, time, items, json
from InquirerPy import inquirer

class Traveller:
    def __init__(self, name):
        self.name = name
        self.job = 'Traveller'
        self.hp = 1
        self.maximum_hp = 1
        self.damage = 1
        self.buffed_damage = 0
        self.defense = 1
        self.buffed_defense = 0
        self.attack_count = 0
        self.weapon_equipped = [False,' ']
        self.basic_skills = ['attack', 'run']
        self.job_skills = ['hit']
        self.unlocked_skills = ['Buff-damage']
        self.other_options = ['status', 'skills', 'bag','save']
        self.basic_skills_description = {"attack" : "based on your damage",
                                         "run" : "don't even try",
                                         "status" : "check status",
                                         "skills" : "check skills"}
        self.job_skills_description = {"hit": "too dangerous"}
        self.unlocked_skills_description = {}
        self.inventory = ['PortionHp5','PortionHpMax','PortionHoly','PortionSuper','Sword','SuperStick']
        self.debuffs = []
        self.buffs = []
        self.finished_chapters = []

    def to_dict(self):
        return self.__dict__

    def from_dict(self, data: dict):
        return self.__dict__.update(data)

    @staticmethod
    def get_job_skills(user, receiver):
        options = {
            'hit': lambda: user.hit(receiver)
        }
        return options

    @staticmethod
    def hit(receiver):
        new_damage = receiver.hp
        receiver.hp -= new_damage
        print(f'you caused {new_damage} damage')


#---------------jobs----------------------------
class Warrior(Traveller):
    def __init__(self, name):
        super().__init__(name)
        self.job = 'Warrior'
        self.hp = 12
        self.maximum_hp = 12
        self.damage = 6
        self.defense = 5
        self.job_skills = ['dimension slash']
        self.job_skills_description = {
            "dimension slash" : "used 2 HP to cause damage based on your hp"
        }

    @staticmethod
    def get_job_skills(user, receiver):
        options = {
            'dimension slash': lambda : user.dimension_slash(user, receiver)
        }
        return options

    @staticmethod
    def dimension_slash(user, receiver):
        if user.hp > 2:
            print('dimension slash!')
            user.hp -= 2
            new_damage = max(user.hp, (user.maximum_hp//2))*2
            receiver.hp -= new_damage
            print(f'you caused {new_damage} damage')
        else:
            print("you don't have enough health")

class Mage(Traveller):
    def __init__(self, name):
        super().__init__(name)
        self.job = 'Mage'
        self.hp = 8
        self.maximum_hp = 8
        self.damage = 9
        self.defense = 3
        self.job_skills = ['ice age']
        self.job_skills_description = {
            "ice age" : "monster's HP halved when when your HP is full"
        }

    @staticmethod
    def get_job_skills(user, receiver):
        options = {
            'ice age': lambda : user.ice_age(user, receiver)
        }
        return options

    @staticmethod
    def ice_age(user, receiver):
        print('ice age!')
        if user.hp == user. maximum_hp:
            new_damage = receiver.hp // 2
            receiver.hp -= new_damage
            print(f'you caused {new_damage} damage')
        else:
            print('magic failed')

class Archer(Traveller):
    def __init__(self, name):
        super().__init__(name)
        self.job = 'Archer'
        self.hp = 10
        self.maximum_hp = 10
        self.damage = 7
        self.defense = 4
        self.job_skills = ['sky break']
        self.job_skills_description = {
            "sky break" : "cause 1.5 times damage based on your current HP, when your HP is lower"
        }

    @staticmethod
    def get_job_skills(user, receiver):
        options = {
            'sky break': lambda : user.sky_break(user, receiver)
        }
        return options

    @staticmethod
    def sky_break(user, receiver):
        if receiver.hp > user.hp:
            print('sky break!')
            new_damage = int(round(user.hp * 1.5,0))
            receiver.hp -= new_damage
            print(f'you caused {new_damage} damage')
        else:
            print(f'{receiver.name} is weaker now')

#-----------------------Monster------------------
class Monster:
    def __init__(self, name, hp, maximum_hp, damage, defense):
        self.name = name
        self.hp = hp
        self.maximum_hp = maximum_hp
        self.damage = damage
        self.buffed_damage = 0
        self.defense = defense
        self.buffed_defense = 0
        self.attack_count = 0
        self.debuff = []
        self.buff = []

    def attack(self, user, receiver):
        attack(user, receiver)

class Hero(Monster):
    def __init__(self, name, hp, maximum_hp, damage, defense):
        super().__init__(name, hp, maximum_hp, damage, defense)
        self.hero_magic_damage = 12

    def attack(self,user, receiver):
        if self.attack_count % 3 == 0:
            hero_magic(receiver)
        else:
            attack(user, receiver)

class DemonKing(Monster):
    def __init__(self, name, hp, maximum_hp, damage, defense):
        super().__init__(name, hp, maximum_hp, damage, defense)
        self.demon_magic_damage = 30

    def attack(self, user, receiver):
        if self.attack_count % 2 == 0:
            demon_magic(receiver)
        else:
            attack(user, receiver)

class Witch(Monster):
    def __init__(self, name, hp, maximum_hp, damage, defense):
        super().__init__(name, hp, maximum_hp, damage, defense)

    def attack(self, user, receiver):
        if self.attack_count in (1, 10):
            receiver.debuffs.append(items.PoisonDebuff(5, 1).to_dict())
            print('Enjoy the suffering of my magic poison')
        else:
            attack(user, receiver)

# --------------------------basic_skills------------------------
def attack(user, receiver):
    damage = random.randint(0, (user.damage + user.buffed_damage))
    defense = random.randint(0, (receiver.defense + receiver.buffed_defense))
    if damage > defense:
        new_damage = damage
        receiver.hp -= new_damage
    else:
        new_damage = damage // 2
        receiver.hp -= new_damage
        print(f'{receiver.name} guarded, damage halved!')
    print(f'{user.name} attacks {new_damage} damage')

def run(user):
    print('You cannot run away')
    user.hp = -100
# -----------------unlocked_skills-------------------------------
def chance_attack(chance, skill_name, skill_damage, success, receiver):
    print(f'{skill_name}!')
    time.sleep(1)
    if random.random() < chance:
        print(f'{success}!')
        print(f'{skill_name} caused {skill_damage} damage')
        receiver.hp -= skill_damage
    else:
        print('nothing happened')

def hero_magic(receiver):
    chance_attack(0.1, 'hero magic', 10, "I'm the hero", receiver)

def demon_magic(receiver):
    chance_attack(0.5, 'demon magic', 20, "Die!", receiver)
#-------------------other_skills--------------------------------
def check_status(user):
    print(f'\ntraveller:{user.name}\n'
          f'job: {user.job}\n'  
          f'HP: {user.hp}/{user.maximum_hp}\n'
          f'equipment: {user.weapon_equipped[1]}\n'
          f'damage: {user.damage}+{user.buffed_damage}\n'
          f'defense: {user.defense}+{user.buffed_defense}\n')

def check_skills(user):
    options = {}
    options.update(user.basic_skills_description)
    options.update(user.job_skills_description)
    options.update(user.unlocked_skills_description)
    for option in options:
        print(f'{option} - {options.get(option)}')

def use_inventory(user):
    choice = inquirer.select(
        message="your bag:",
        choices= user.inventory + ['disarm','back'],
        qmark=":>"
    ).execute()

    if choice  == 'back':
        return
    elif choice == 'disarm':
        items.disarm(user)
    else:
        items.Item.all_item.get(choice)().use(user)
# -------------------skills_merge-------------------------------
def get_basic_skills(user, receiver):
    options = {
        'attack' : lambda: attack(user, receiver),
        'run': lambda: run(user)
    }
    return options

def get_unlocked_skills(user, receiver):
    options = {
        'hero magic': lambda: hero_magic(receiver),
        'demon magic': lambda: demon_magic(receiver),
        'Buff-damage':lambda: buff_add(user, (items.DamageBuff(3, 5, False).to_dict()))
    }
    return options

def get_other_options(user):
    options = {
        'bag': lambda : use_inventory(user),
        'status': lambda:check_status(user),
        'skills': lambda:check_skills(user),
        'save' : lambda: save_game(user),
    }
    return options

def available_skills(user, receiver):
    options = {}
    options.update(get_basic_skills(user, receiver))
    options.update(user.get_job_skills(user, receiver))
    options.update(get_unlocked_skills(user, receiver))
    options.update(get_other_options(user))
    return options

def show_all_skills(user):
    return user.basic_skills + user.job_skills + user.unlocked_skills + user.other_options
# ----------------others-----------------------------------------
def check_debuff(receiver):
    active_effects = []
    debuffs = []
    for debuff in receiver.debuffs:
        name = debuff['name']
        duration = debuff['duration']
        amount = debuff['amount']
        debuffs.append(items.buff_transform[name](duration, amount))

    for effect in debuffs:
        if effect.tick(receiver):
            active_effects.append(effect.to_dict())
    receiver.debuffs = active_effects

def check_buff(user):
    active_effects = []
    buffs = []
    for buff in user.buffs:
        name = buff['name']
        duration = buff['duration']
        amount = buff['amount']
        activate = buff['activate']
        buffs.append(items.buff_transform[name](duration, amount, activate))

    for effect in buffs:
        if effect.tick(user):
            active_effects.append(effect.to_dict())
    user.buffs = active_effects

def buff_add(user,buff):
    for b in user.buffs:
        if b['name'] == buff['name']:
            b['duration'] = max(b['duration'], buff['duration'])
            return
    user.buffs.append(buff)

def save_game(user):
    with open ("save.json", "r+") as f:
        data = json.load(f)
        new_data = {f'{user.name}-{user.job}' : user.to_dict()}
        data.update(new_data)
        f.seek(0)
        json.dump(data, f, indent=4)

def load_game(user):
    with open("save.json", "r",encoding="utf-8") as f:
        data = json.load(f)
        if f'{user.name}-{user.job}' in data.keys():
            user.from_dict(data[f'{user.name}-{user.job}'])
            print(f'Welcome back, Great {user.job}, {user.name}!')
        else:
            print(f"I know nothing about you, {user.job}. {user.name} right?")


def remove_save(name,job):
    with open("save.json", "r",encoding="utf-8") as f:
        data = json.load(f)
        data.pop(f'{name.lower().capitalize()}-{job.lower().capitalize()}')
    with open("save.json", "w",encoding="utf-8") as f:
        json.dump(data, f, indent=4)

