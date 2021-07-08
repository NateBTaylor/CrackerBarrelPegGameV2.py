import pygame
import random
import sys


pygame.init()

in_game = True
screen = pygame.display.set_mode((750, 750))
pygame.display.set_caption("Cracker Barrel Game")
my_font = pygame.font.SysFont('Comic Sans MS', 50)

clock = pygame.time.Clock()

pos_to_place = {1: [0, 0], 2: [1, 0], 3: [1, 1], 4: [2, 0], 5: [2, 1],
                6: [2, 2], 7: [3, 0], 8: [3, 1], 9: [3, 2], 10: [3, 3],
                11: [4, 0], 12: [4, 1], 13: [4, 2], 14: [4, 3], 15: [4, 4]}

moves = {1:[[4, 2], [6, 3]], 2:[[7, 4], [9, 5]], 3: [[8, 5], [10, 6]],
        4: [[11, 7], [13, 8], [1, 2], [6, 5]], 5: [[12, 8], [14, 9]], 6: [[1, 3], [4, 5], [15, 10], [13, 9]],
        7: [[2, 4], [9, 8]], 8: [[10, 9], [3, 5]], 9: [[2, 5], [7, 8]],
        10: [[8, 9], [3, 6]], 11: [[4, 7], [13, 12]], 12: [[5, 8], [14, 13]],
        13: [[11, 12], [15, 14], [4, 8], [6, 9]], 14: [[12, 13], [5, 9]], 15: [[6, 10], [13, 14]]}

peg_list = []
select = []

score = 0
game_over = False

peg_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

class Peg:
  def __init__(self, size, color, filled, row, col, pos, pc, id, selected):
    self.size = size
    self.color = color
    self.filled = filled
    self.row = row
    self.col = col
    self.pos = pos
    self.pc = pc
    self.id = id
    self.selected = selected
    
  def draw(self):
    pygame.draw.rect(screen, (0, 0, 0), [self.pos[0], self.pos[1], self.size, self.size], 5)
    pygame.draw.rect(screen, self.color, [self.pos[0] + 2.5, self.pos[1] + 2.5, self.size - 5, self.size -  5])
    if self.filled:
      pygame.draw.circle(screen, self.pc, (round(self.pos[0] + self.size / 2), round(self.pos[1] + self.size / 2)), 15)

def set_pegs():
  global peg_list, peg_colors
  count = 1
  id = 1
  pos = [0, 50]
  for i in range(5):
    pos[0] = 375 - (count / 2) * 100
    if count == 1:
      filled = False
    else:
      filled = True
    for j in range(count):
      peg_list.append(Peg(100, (255, 255, 255), filled, i, j, [pos[0], pos[1]], random.choice(peg_colors), id, False))
      id += 1
      pos[0] += 100
    count += 1
    pos[1] += 100

set_pegs()

def find_peg(pn):
  for peg in peg_list:
    if peg.id == pn:
      return peg
      
def find_options(peg):
  global moves
  options = []
  for key, value in moves.items():
    if key == peg.id and peg.filled:
      for i in range(len(value)):
        fp = find_peg(moves[key][i][0])
        mp = find_peg(moves[key][i][1])
        if fp.filled == False and mp.filled:
          options.append(moves[key][i][0])
  return options

def check_game_over():
  global peg_list
  count = 0
  for peg in peg_list:
    if len(find_options(peg)) > 0:
      count += 1
    else:
      count = count
  return count < 1

def check_move():
  if len(select) > 1:
    if select[1].color == (185, 189, 196):
      return 'jump'
    elif select[1].color != (185, 189, 196):
      return 'us'
  else:
    return False
      
def get_score():
  global peg_list
  score = 0
  for peg in peg_list:
    if peg.filled:
      score += 1
  return score
  
def unselect_peg(peg):
  global select
  pegs = find_options(peg)
  for i in pegs:
    option = find_peg(i)
    option.color = (255, 255, 255)
  peg.selected = False
  select.remove(peg)
  peg.color = (255, 255, 255)

def jump_peg(start_peg, end_peg):
  global moves, game_over, score
  unselect_peg(start_peg)
  start_peg.filled = False
  end_peg.filled = True
  end_peg.pc = start_peg.pc
  for key, value in moves.items():
    if key == start_peg.id:
      for i in range(len(value)):
        if moves[key][i][0] == end_peg.id:
          mp = find_peg(moves[key][i][1])
          mp.filled = False
  if check_game_over():
    score = get_score()
    game_over = True
    print('game over')
  

def select_peg(peg):
  global select
  select.append(peg)
  if check_move() == 'jump':
    jump_peg(select[0], select[1])
  elif check_move() == 'us':
    unselect_peg(select[0])
  pegs = find_options(peg)
  for i in pegs:
    option = find_peg(i)
    option.color = (185, 189, 196)
  pegs.clear()
  peg.selected = True
  peg.color = (135, 129, 145)

def display_text(text, x, y, color):
  text = my_font.render(text, False, color)
  screen.blit(text, (x, y))

while in_game:
  
  screen.fill((0, 0, 255))
  
  for peg in peg_list:
    peg.draw()
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      in_game = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()
      chosen_peg = [peg for peg in peg_list if pygame.Rect(peg.pos[0], peg.pos[1], peg.size, peg.size).collidepoint(mouse_pos)]
      if len(chosen_peg) > 0:
        if chosen_peg[0].selected == False:
          select_peg(chosen_peg[0])
        else:
          unselect_peg(chosen_peg[0])
  
  display_text("Cracker Barrel Game", 180, 10, (255, 255, 255))
  
  if game_over:
    display_text("Game Over, final score is: " + str(score), 150, 555, (255, 255, 255))
  
  pygame.display.update()
  clock.tick(60)


pygame.quit()
quit()