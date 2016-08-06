import libtcodpy as libtcod
from Object import Object
from Tile import Tile
from Dungeon import Rect

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 50

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 40

LIMIT_FPS = 20

con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
npc = Object(SCREEN_WIDTH/2-5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
objects = [npc, player]

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD);
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'example window', False);
libtcod.sys_set_fps(LIMIT_FPS);

def handle_keys():
  dx=0
  dy=0
  key = libtcod.console_wait_for_keypress(True);
  
  if libtcod.console_is_key_pressed(libtcod.KEY_UP):
    dy=-1
    if not map[player.x+dx][player.y+dy].blocked:
      player.move(0, -1)

  elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
    dy=1
    if not map[player.x+dx][player.y+dy].blocked:
      player.move(0, 1)

  elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
    dx=-1
    if not map[player.x+dx][player.y+dy].blocked:
      player.move(-1, 0)

  elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
    dx=1
    if not map[player.x+dx][player.y+dy].blocked:
      player.move(1, 0)

  if key.vk == libtcod.KEY_ESCAPE:
    return True



def create_room(room):
  global map
  for x in range(room.x1+1, room.x2):
    for y in range(room.y1+1, room.y2):
      map[x][y].blocked = False
      map[x][y].block_sight = False

def create_h_tunnel(x1,x2,y):
  global map
  for x in range(min(x1, x2), max(x1,x2) +1):
    map[x][y].blocked = False
    map[x][y].block_sight = False

def create_v_tunnel(y1,y2,x):
  global map
  for y in range(min(y1,y1),max(y1,y2)+1):
    map[x][y].blocked = False
    map[x][y].block_sight = False

def make_map():
  global map
  map = [[Tile(True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

  rooms = []
  num_rooms = 0

  for r in range(MAX_ROOMS):
    w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)

    x = libtcod.random_get_int(0,0,MAP_WIDTH - w - 1)
    y = libtcod.random_get_int(0,0,MAP_HEIGHT - h - 1)

    new_room = Rect(x,y,w,h)

    failed = False
    for other_room in rooms:
      if new_room.intersect(other_room):
        failed=True
        break

    if not failed:
      create_room(new_room)
      (new_x,new_y) = new_room.center()
      #optional: print "room number" to see how the map drawing worked
      #we may have more than ten rooms,
      ##so print 'A' for the first room, 'B' for the next...
      room_no = Object(new_x, new_y, chr(65+num_rooms), libtcod.white)
      objects.insert(0, room_no) #draw early, so monsters are drawn on top

      if num_rooms == 0:
        player.x = new_x
        player.y = new_y

      else:
        (prev_x,prev_y) = rooms[num_rooms-1].center()
        if libtcod.random_get_int(0,0,1) ==1:
          create_h_tunnel(prev_x, new_x, prev_y)
          create_v_tunnel(prev_y, new_y, new_x)
        else:
          create_v_tunnel(prev_y, new_y, prev_x)
          create_h_tunnel(prev_x, new_x, new_y)
          
      rooms.append(new_room)
      num_rooms +=1
      
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
