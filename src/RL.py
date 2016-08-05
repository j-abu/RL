import libtcodpy as libtcod
from Object import Object
from Tile import Tile

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 50

LIMIT_FPS = 20

con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
npc = Object(SCREEN_WIDTH/2-5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
objects = [npc, player]

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD);
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'example window', False);
libtcod.sys_set_fps(LIMIT_FPS);

def handle_keys():
  
  key = libtcod.console_wait_for_keypress(True);

  if libtcod.console_is_key_pressed(libtcod.KEY_UP):
    player.move(0, -1)

  elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
    player.move(0, 1)

  elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
    player.move(-1, 0)

  elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
    player.move(1, 0)

  if key.vk == libtcod.KEY_ESCAPE:
    return True

def make_map():
  global map
  map = [[Tile(False) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

def render_all():
  ##global color_wall
  ##global color_ground 

  for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
      wall = map[x][y].block_sight
      if wall:
        libtcod.console_set_char_background(con, x, y, '#', libtcod.black)
        libtcod.console_put_char(con, x, y, '#', libtcod.white)
      else:
        libtcod.console_set_char_background(con, x, y, '.', libtcod.black)
        libtcod.console_put_char(con, x, y, '.', libtcod.white)

  for object in objects:
    object.draw(con)

  libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

make_map()

##main game loop

while not libtcod.console_is_window_closed():

  render_all()
  libtcod.console_flush()

  for object in objects:
    object.clear(con)

  exit = handle_keys();
  if exit:
    break
