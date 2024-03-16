#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <cmath>


enum class Orientation {
  East = 0, North = 1, West = 2, South = 3
};

std::ostream & operator<<(std::ostream & os, const Orientation o) {
  switch (o) {
    case Orientation::East: return os << "East";
    case Orientation::West: return os << "West";
    case Orientation::North: return os << "North";
    case Orientation::South: return os <<  "South";
    default: break;
  }
  return os << "Unknown";
}

enum class Direction {
  Forward = 'F', Left = 2, Right = 3
};

class Ship {
public:
  void Follow(const std::string);
  int Manhattan() const { return std::abs(xd) + std::abs(yd); }
private:
  Orientation orientation{Orientation::East};
  int xd{0}, yd{0};
};

Orientation Turn(Orientation o, char dir, int deg) {
  deg %= 360;
  int amt = deg / 90;
  if (dir == 'R') amt = -amt;
  return (Orientation)(((int)o + amt + 4) % 4);
}


void Ship::Follow(const std::string s) {
  char d;
  int amt;
  std::stringstream ss{s};
  ss >> d >> amt;
  switch (d) {
    case 'F':
      switch (orientation) {
        case Orientation::East: xd += amt; break;
        case Orientation::West: xd -= amt; break;
        case Orientation::North: yd += amt; break;
        case Orientation::South: yd -= amt; break;
      }
      break;
    case 'L': case 'R':
      orientation = Turn(orientation, d, amt);
      break;
    case 'N': yd += amt; break;
    case 'S': yd -= amt; break;
    case 'W': xd -= amt; break;
    case 'E': xd += amt; break;
  }
}



int main() {
  std::fstream ifs{"input.txt"};
  int xd{0}, yd{0};
  Ship ship;
  std::string cmd;
  while (std::getline(ifs, cmd)) {
    ship.Follow(cmd);
  }
  std::cout << "Manhattan: " << ship.Manhattan() << '\n';



}
