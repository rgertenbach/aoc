from beacon import Axis, Beacon, Point, point_matches
from typing import List, Optional

class Scanner:
  reach = 1000
  
  @classmethod
  def parse(cls, f, scanner_id):
    beacons = f.split('\n')[1:]
    beacons = [beacon.split(',') for beacon in beacons if beacon]
    beacons = [Beacon(int(x), int(y), int(z)) for x, y, z in beacons]
    return cls(beacons, scanner_id)
  

  def __init__(self, beacons: Optional[List[Beacon]] = None, scanner_id=None):
    self.beacons = beacons
    self.scanner_id = scanner_id

  def __str__(self):
    beacons = [f'  {str(beacon)}' for beacon in self.beacons]
    return f'Scanner {self.scanner_id}:\n' + '\n'.join(beacons)

  def __add__(self, direction) -> 'Scanner':
    out = self.__class__(scanner_id=self.scanner_id)
    out.beacons = [beacon + direction for beacon in self.beacons]
    return out

  def __sub__(self, direction) -> 'Scanner':
    out = self.__class__(scanner_id=self.scanner_id)
    out.beacons = [beacon - direction for beacon in self.beacons]
    return out

  def copy(self) -> 'Scanner':
    out = self.__class__()
    out.beacons = [beacon.copy() for beacon in self.beacons]
    out.scanner_id = self.scanner_id
    return out

  def permutations(self) -> List['Scanner']:
    perms = [beacon.permutations() for beacon in self.beacons]
    return [Scanner(beacons, self.scanner_id) for beacons in zip(*perms)]

  def overlaps(self, other: 'Scanner', thresh: int = 12):
    'A list of possible overlaps'

    for sb in self.beacons[:-11]:
      sc = self - sb
      for ob in other.beacons:
        oc = other - ob
        matches = point_matches(sc.beacons, oc.beacons)
        if len(matches) >= thresh:
          return [match + sb for match in matches] 

  def merge(self, other, thresh: int = 12) -> Optional['Scanner']:
    for sb in self.beacons[:-11]:
      sc = self - sb
      for ob in other.beacons:
        oc = other - ob
        matches = point_matches(sc.beacons, oc.beacons)
        if len(matches) >= thresh:
          # return [match + sb for match in matches] 
          obs = (other - ob + sb).beacons
          # obs = [o - ob + sc for o in other.beacons]
          return self.__class__(self.beacons + obs).dedupe()

  def dedupe(self) -> 'Scanner':
    beacons = list(set(self.beacons))
    return self.__class__(beacons, self.scanner_id)
    
