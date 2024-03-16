#include <iostream>
#include <fstream>
#include <vector>
#include <cctype>
#include <algorithm>

class Schedule {
public:
  Schedule(std::istream&);
  const std::vector<int>& Buses() const { return buses;}
  int Earliest() const {return earliest;}
private:
  int earliest;
  std::vector<int> buses;
};


Schedule::Schedule(std::istream& is) {
  is >> earliest;
  while (is) {
    int bus;
    is >> bus;
    buses.push_back(bus);
    int c;
    while (is && !std::isdigit((c = is.get())));
    is.putback(c);
  }
}


int main() {
  std::fstream ifs{"input.txt"};
  Schedule s{ifs};
  int soonest_bus, soonest_time;
  for (int i = 0; i <s.Buses().size(); ++i) {
    int time =  s.Buses()[i] * (s.Earliest() / s.Buses()[i] + 1);
    if (i == 0 || time < soonest_time) {
      soonest_bus = s.Buses()[i];
      soonest_time = time;
    }
  }

  std::cout << soonest_bus * (soonest_time - s.Earliest());

}
