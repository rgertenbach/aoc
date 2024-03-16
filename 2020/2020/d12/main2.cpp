#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <cmath>

struct Point {
  int x, y;
};

Point operator+(const Point &p1, const Point &p2) {
  return Point{p1.x + p2.x, p1.y + p2.y};
}
Point operator*(const Point &p1, const int x) {
  return Point{p1.x * x, p1.y * x};
}
Point operator+=(Point &p1, const Point &p2) {
  p1 = p1 + p2;
  return p1;
}
std::ostream& operator<<(std::ostream& os, const Point p) {
  return os << '(' << p.x << ',' << p.y << ')';
}

class Ship {
public:
  void Follow(const std::string);
  int Manhattan() const { return std::abs(loc.x) + std::abs(loc.y); }
private:
  Point loc{0, 0};
  Point vec{10, 1};
};

Point Turn(Point p, char dir, int deg) {
  deg %= 360;
  if (dir == 'L' && deg == 90) deg = 270;
  else if (dir == 'L' && deg == 270) deg = 90;
  switch (deg) {
    case 90: return Point{p.y, -p.x};
    case 180: return Point{-p.x, -p.y};
    case 270: return Point{-p.y, p.x};
    default: return p;
  }
}

void Ship::Follow(const std::string s) {
  char d;
  int amt;
  std::stringstream ss{s};
  ss >> d >> amt;
  switch (d) {
    case 'F': loc += vec * amt; break;
    case 'L': case 'R': vec = Turn(vec, d, amt); break;
    case 'N': vec.y += amt; break;
    case 'S': vec.y -= amt; break;
    case 'W': vec.x -= amt; break;
    case 'E': vec.x += amt; break;
  }
}

int main() {
  std::fstream ifs{"input.txt"};
  Ship ship;
  std::string cmd;
  while (std::getline(ifs, cmd)) ship.Follow(cmd);
  std::cout << "Manhattan: " << ship.Manhattan() << '\n';
}
