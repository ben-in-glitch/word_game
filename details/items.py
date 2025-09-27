def wear(user, item, damage):
    if not user.weapon_equipped[0]:
        user.weapon_equipped[1] = item
        user.buffed_damage += damage
        print(f"{item} has been equipped: damage + {damage}")
        user.weapon_equipped[0] = True
        used_remove(user, item)

    else:
        print(f"only one weapon can be equipped")

def disarm(user):
    if user.weapon_equipped[0]:
        damage = Item.all_item[user.weapon_equipped[1]]().damage
        user.buffed_damage -= damage
        user.inventory.append(user.weapon_equipped[1])
        print(f"{user.inventory[-1]} is in your bag now")
        user.weapon_equipped = [False, ' ']

    else:
        print("no weapon is equipped")


def heal(user, item, amount):
    before = user.hp
    user.hp = min(user.maximum_hp, user.hp + amount)
    print(f'{item} healed {user.hp - before}')


def used_remove(user, item):
    user.inventory.remove(item)

class Item:
    all_item = {}

    def __init__(self):
        self.name = ""
        self.damage = 0

    def use(self, user):
        wear(user, self.name, self.damage)

    def disarm_damage(self):
        return self.damage

    @classmethod
    def register(cls,cls_name):
        cls.all_item[cls_name.__name__] = cls_name
        return cls_name

@Item.register
class PortionHp5(Item):
    def __init__(self):
        super().__init__()
        self.name = 'PortionHp5'
        self.amount = 5

    def use(self, user):
        heal(user, self.name, self.amount)
        used_remove(user, self.name)


@Item.register
class PortionHpMax(Item):
    def __init__(self):
        super().__init__()
        self.name = 'PortionHpMax'
        self.amount = 9999

    def use(self, user):
        heal(user, self.name, self.amount)
        used_remove(user, self.name)


@Item.register
class PortionHoly(Item):
    def __init__(self):
        super().__init__()
        self.name = 'PortionHoly'
        self.amount = 0

    def use(self, user):
        user.debuffs.clear()
        print('All debuff removed')
        used_remove(user, self.name)

@Item.register
class PortionSuper(Item):
    def __init__(self):
        super().__init__()
        self.name = 'PortionSuper'
        self.maximum_hp = 1000
        self.buffed_defense = 1000
        self.buffed_damage = 1000

    def use(self, user):
        user.maximum_hp = self.maximum_hp
        user.hp += 1000
        user.buffed_defense += self.buffed_defense
        user.buffed_damage += self.buffed_damage
        print('You are invincible now')
        used_remove(user, self.name)

@Item.register
class Sword(Item):
    def __init__(self):
        super().__init__()
        self.name = 'Sword'
        self.damage = 2

@Item.register
class SuperStick(Item):
    def __init__(self):
        super().__init__()
        self.name = 'SuperStick'
        self.damage = 100


#--------------------buff/debuff----------------------
class Effects:
    def __init__(self, name, duration, amount):
        self.name = name
        self.duration = duration
        self.amount = amount

    def to_dict(self):
        return self.__dict__

    def tick(self,receiver):
        raise NotImplementedError

class Buff(Effects):
    def __init__(self, name, duration, amount):
        super().__init__(name, duration, amount)

    def tick(self,receiver):
        raise NotImplementedError


class DamageBuff(Buff):
    def __init__(self, duration, amount,activate):
        super().__init__('DamageBuff', duration, amount)
        self.activate = activate

    def tick(self,user):
        if not self.activate:
            print(f'{self.name} on, damage+{self.amount}')
            user.buffed_damage += self.amount
            self.activate = True
        else:
            print(f'{self.name} is activating: duration {self.duration}')

        if self.duration <= 0:
            user.buffed_damage -= self.amount
            self.activate = False
            return self.activate

        self.duration -= 1
        return self.activate


class Debuff(Effects):
    def __init__(self, name, duration, amount):
        super().__init__(name, duration, amount)

    def tick(self,receiver):
        raise NotImplementedError


class PoisonDebuff(Debuff):
    def __init__(self, duration, amount):
        super().__init__('PoisonDebuff', duration, amount)


    def tick(self, receiver):
        print(f'Debuffing HP -{self.amount}, duration: {self.duration}')
        receiver.hp -= self.amount
        self.duration -= 1
        return self.duration > 0

buff_transform = {
    'DamageBuff': DamageBuff,
    'PoisonDebuff': PoisonDebuff,
}






