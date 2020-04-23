import numpy as np

import random
# from random import randint

# ========================================================================= #
#
# The world is a rectangle:
#
# 1. Domain: Nx * Ny
# 2. Grid coordinate: ix, iy
# 3. Periodic condition: is_periodic_x, is_periodic_y
# 4. Smallest time interval: dt
#
# ========================================================================= #


# ========================================================================= #
#
# The creature attributes:
#
# 1. Strength: strength (att_str)
#    - melee damage       : dmg_melee
#    - range damage       : dmg_range
#    - stamina consumption: dst, how much stamina is consumed
#                           every dt, the more att_str, the more consumption
# 2. Dexterity: dexterity (att_dex)
#    - attack interval: ack_ndt, time interval per between two attacks
#    - attack roll    : ack_roll, if it is equal or over defence roll, attack is successful
#    - defence roll   : def_roll, if it is over the attack roll, no damage
#    - move speed     : spd, how many moves you can make every dt
# 3. Constitution: constitution (att_con)
#    - max hit points: hp_max
#    - hp recovery   : dhp, how many hp is recovered every dt
#    - max stamina   : st_max, attack (physics and spell) consumes stamina
#    - damage block  : dmg_blk, how many damage is reduced for every hit
# 4. Intelligence: intelligence (att_int)
#    - max mana points: mp_max
#    - mana recovery  : dmp, how many mp is recovered every dt
#    - spell damage   : dmg_spell
# 5. Charisma: charisma (att_cha)
#    - leadership: lead, how much you can increase the ability of a group
#    - teamwork  : team, how much ability is increased in a group
#    - persuasion: pers, how possible you can persuade a creature to be
#                  grouped with you
#
# Other properties:
#
# 1. Group: group, which group or teams you are in
# 2. Base damage: dmg_base, every creature has a base damage
# 3. Base stamina: st_base
# 4. Base hp: hp_base
# 5. Base mp: mp_base
# 6. Base attack interval: ack_ndt_base
# 7. Base attack: ack_base
# 8. Base defence: def_base
# 9. Base move speed: spd_base
# 10. Base 
#
# Statistics:
# 1. damage: dmg
#
# ========================================================================= #

def d(sides):
  return random.randint(1, sides)


def roll(n, sides):
  return tuple(d(sides) for _ in range(n))


def dice(n, sides):
  return sum(roll(n, sides))


class Map:
  def __init__(self, Nx, Ny, is_periodic_x=True, is_periodic_y=False):
    self.Nx = Nx
    self.Ny = Ny
    # 2D array saving the block status
    # 0: empty
    # 1: there is a creature
    self.block = np.zeros( (Ny, Nx) )

    self.is_periodic_x = is_periodic_x
    self.is_periodic_y = is_periodic_y



class Creature:
  # Every creature has a unique id
  current_id = 0

  def __init__(self, x, y, playmap):
    # HP
    self.hp_base = 10
    self.hp_max = self.hp_base + dice(1,10)
    self.hp = self.hp_max

    # Damage
    self.dmg = dice(1, 5)

    # Position
    self.x = x
    self.y = y

    # Set creature in the map
    playmap.block[y, x] = Creature.current_id
    current_id += 1


  def move(self, direction):
    if direction == 0:  # up
      self.dy = -1
    elif direction == 1:  # right
      self.dx = 1
    elif direction == 2:  # down
      self.dy = 1
    elif direction == 3:  # left
      self.dx = -1
    else:
      print('Wrong direction.')


  def update(self, playmap):
    pos_dest_x = self.x + self.dx
    pos_dest_y = self.y + self.dy
    if playmap[pos_dest_y, pos_dest_x] == 1:
      self.attack(



  def attack(self, creature):
    creature.hp -= self.dmg



if __name__ == '__main__':
  random.seed()

  playmap = Map(100, 100)

  print(d(10))
  dice = roll(3,10)
  print(dice)
  print(sum(dice))
