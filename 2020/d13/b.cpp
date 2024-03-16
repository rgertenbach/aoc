#include <iostream>
#include <fstream>
#include <vector>
#include <cctype>
#include <algorithm>
#include <limits>

struct Bus { int index, time; };

std::vector<Bus> *LoadTimes(std::istream & is) {
  std::vector<Bus> *buses = new std::vector<Bus>;
  int i{0};
  is.ignore(std::numeric_limits<std::streamsize>::max(), '\n');  // Earliest time, ignored here.
  while (is) {
    int bus, c;
    is >> bus;
    buses->push_back(Bus{i, bus});
    while (is && !std::isdigit((c = is.get()))) if (c == ',') ++i;
    is.putback(c);
  }
  return buses;
}

int main() {
  std::fstream ifs{"input.txt"};
  std::vector<Bus> *times = LoadTimes(ifs);
  for (Bus bus : *times) std::cout << bus.index << " (" << bus.time << ")\t";
}


// x0 * 17 = x2 * 13 - 2
// 17 * 13 = 221:q

