from typing import Iterable, List
import enum

# Cave Node IDs (Rooms):
# 0  1  2  3  4  5  6  7  8  9 10
#      11    13    15    17
#      12    14    16    18
CONNS = {
  0:  [1],
  1:  [0, 2],
  2:  [1, 3, 11],
  3:  [2, 4],
  4:  [3, 5, 13],
  5:  [4, 6],
  6:  [5, 7, 15],
  7:  [6, 8],
  8:  [7, 9, 17],
  9:  [8, 10],
  10: [9],
  11: [2, 12],
  12: [11],
  13: [4, 14],
  14: [13],
  15: [6, 16],
  16: [15],
  17: [8, 18],
  18: [17],
}

HOME_ROOMS = {
  'a': [11, 12],
  'b': [13, 14],
  'c': [15, 16],
  'd': [17, 18]}

EMPTY = '.'

COST = {
  'a': 1,
  'b': 10,
  'c': 100,
  'd': 1000}

class Pod:
  def __init__(self, color: str, room: int, is_moving: bool = False):
    self.color = color
    self.room = room
    self.is_moving = is_moving

  @property
  def is_home(self) -> bool:
    return self.room in HOME_ROOMS[self.color]

  def in_hallway(self) -> bool:
    return self.room < 10

  def __str__(self) -> str:
    return f'{self.color}: {self.room}'
    

class Cave:
  def __init__(self, pods: Iterable[Pod]):
    self.pods = list(pods)

  def content(self, room: int):
    pod = [pod for pod in self.pods if pod.room == room]
    if pod:
      return pod[0].color
    return EMPTY

  def __str__(self) -> str:
    {self.content(room) for room in range(19)}
    s = '#############\n#'
    contents = [self.content(room) for room in range(19)]
    for i in range(11):
      s += contents[i]
    s += '#\n###'
    s += f'{contents[11]}#{contents[13]}#{contents[15]}#{contents[17]}###\n'
    s += f'  #{contents[12]}#{contents[14]}#{contents[16]}#{contents[18]}#\n'
    s += '  #########'
    return s

  @property
  def to_move(self) -> List[Pod]:
    'All pods that are not home or are above a forein one in their home.'
    out = []
    for color in 'abcd':
      col_pods = [pod for pod in self.pods if pod.color == color]
      home_pods = [pod for pod in self.pods if pod.is_home]
      lowest_wrong = max([pod for pod in home_pods if pod.color != color], 
                         key=lambda p: p.room)
      for pod in col_pods:
        if pod.room not in HOME_ROOMS[color] or pod.room < lowest_wrong.room:
          out.append(pod)
    return out

  def accessible(self, color: str) -> bool:
    pods = [pod for pod in self.pods if pod.room in HOME_ROOMS[color]]
    return min(pods, key=lambda p: p.room).room > HOME_ROOMS[color]

  def pure(self, color: str) -> bool:
    pods = [pod for pod in self.pods if pod.room in HOME_ROOMS[color]]
    return all(pod.color == color for pod in pods)

  @property
  def can_move(self) -> List[Pod]:
    'All pods that can move (need to move at some point and are able to.'
    to_move = self.to_move
    out = []
    # Add all pods that are in the hallway and can go home.
    for pod in to_move:
      if pod.in_hallway and self.accessible(pod.color) and self.pure(pod.color):
        out.append(pod)

    to_move = [pod for pod in to_move if pod not in out]
    # Add all pods that are in the wrong home

    # Add all pods that are in the right home but above 

    # filter pods for ones that can move into *a* room

  
