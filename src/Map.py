import libtcodpy as libtcod

MAP_WIDTH = 50
MAP_HEIGHT = 50

color_wall = libtcod.Color(0,0,100)
color_ground = libtcod.Color(50,50,150)

class Tile:
  def __init__(self, blocked, block_sight = None):
    self.blocked = blocked

    if block_sight is None: block_sight = blocked
    self.block_sight = block_sight


def make_map():
  global map
  map = [[Tile(False) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
