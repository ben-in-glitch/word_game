import random
from tkinter.font import names
from winreg import KEY_NOTIFY


class Player:
    def __init__(self):
        self.basic_skills = ['basic']
        self.your_skills = [['a',lambda : 10*10], ['b','b+2'], ['c','23']]
        self.job_skills = ['z', 'y']
        self.skill_list = {
            'a': 10,
            'b': 20
        }

    def show_your_skills(self):
        print(f'{self.basic_skills}, {self.your_skills}')

    def show_skill_list(self):
        print(self.skill_list)

    def all_skills(self):
        return self.basic_skills + self.your_skills + self.job_skills

class Warrior(Player):
    def __init__(self):
        super().__init__()
        self.your_skills = ['hre']
        self.skill_list2 = {
            'c' : 30
        }

# # print(ben.your_skills[0][1]())
# for i in ben.your_skills:
#     if 'a' in i[0]:
#         print(ben.your_skills[0][1]())

# skill_list = {
#     'a': 10,
#     'b': 20,
#     'c': lambda: 6*6
# }
# result = map('c', skill_list)
# print(result)

# from InquirerPy import inquirer
#
# choice = inquirer.select(
#     message="選擇你的動作:",
#     choices=["攻擊", "防禦", "技能", "逃跑"],
# ).execute()
#
# print(f"你選擇了 {choice}")

a = [{
    'name' : 'DamageBuff',
    'duration' : '2',
    'amount' : '3'
},
    {'name' : 'DefenseBuff',
    'duration' : '6',
    'amount' : '4'}
    ]
b = {
    'd' : '4',
    'e' : '5',
}
buff = []
for i in a:
    buff.append(f'{i["name"]}({i['duration']}, {i['amount']})')
print(buff)



# merge_2 = {**a,**b}
# print(merge_2)
# options = {}
# options.update(a)
# options.update(b)
# for i in options:
#     print(i,options.get(i))



# def attack(attacker, defender):
#     damage = random.randint(1, attacker.damage)
#     defense = random.randint(1, defender.defense)
#     if damage > defense:
#         new_damage = damage
#         defender.hp -= new_damage
#     else:
#         new_damage = damage // 2
#         defender.hp -= new_damage
#         print(f'{defender.name} guarded, damage halved!')
#     print(f'{attacker.name} attacks {new_damage} damage')


