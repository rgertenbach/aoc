#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

struct Range { int low, high; };
struct Field { Range first, second; };
using Ticket = std::vector<int>;

std::istream& operator>>(std::istream& is, Range& f) {
  is >> f.low;
  is.get();
  return is >> f.high;
}

std::ostream& operator<<(std::ostream& os, const Range& f) {
  return os << f.low << '-' << f.high;
}

std::istream& operator>>(std::istream& is, Field& f) {
  is.ignore(99, ' ');
  std::string o;
  return is >> f.first >> o >> f.second;
}

std::ostream& operator<<(std::ostream& os, const Field& f) {
  return os << f.first << " or " << f.second;
}

std::istream& operator>>(std::istream& is, Ticket& t) {
  int x;
  while (is) {
    is >> x;
    if (is) t.push_back(x);
    is.ignore(1);
  }
  return is;
}

std::ostream& operator<<(std::ostream& os, const Ticket& t) {
  for (int x : t) os << x << ' ';
  return os;
}

void geticket(std::istream& is, Ticket& t) {
  std::string line;
  std::getline(is, line);
  std::stringstream l{line};
  l >> t;
}

void getfield(std::istream& is, Field& f) {
  std::string line;
  std::getline(is, line);
  std::stringstream l{line};
  l >> f;
}

int main() {
  std::vector<Field> fields;
  Ticket ticket;
  std::vector<Ticket> others;
  std::string line;
  std::ifstream ifs{"test.txt"}; 
  while (ifs) {
    std::getline(ifs, line);
    if (!line.length()) break;
    std::stringstream l{line};
    Field f;
    l >> f;
    fields.push_back(f);
  }
  ifs.ignore(1000, '\n');
  getticket(ifs, ticket);

  ifs.ignore(1000, '\n');
  while (ifs.good()) {
    Ticket other;
    getticket(ifs, other);
    others.push_back(other);
  }
  std::cout << ticket << '\n';
  for (Ticket t : others) {
    std::cout << t << '\n';
  }
}
