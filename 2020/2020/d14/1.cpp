#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <iomanip>

long long int ApplyMask(long long int x, const std::string mask) {
  for (int i = 0; i < mask.length(); ++i) {
    long long int m = 1LL << (mask.size() - i - 1);
    switch (mask[i]) {
      case '1': x |= m; break;
      case '0': x &= (~m); break;
      default: break;
    }
  }
  return x;
}


int main() {
  typedef std::map<int, long long int> Memory;
  std::ifstream is{"input.txt"};
  std::string mask{""};
  Memory memory;

  while (true) {
    std::string lvalue;
    char c;
    is >> lvalue >> c;
    if (!is) break;  // We can safely expect an rvalue.
    if (lvalue == "mask") {
      std::string rvalue;
      is >> mask;
    } else { // lvalue == "mem[idx]"
      int idx;
      long long int rvalue;
      is >> rvalue;
      std::stringstream lval{lvalue};
      lval.ignore(10, '['); // Should only be 3 and [.
      lval >> idx;
      memory[idx] = ApplyMask(rvalue, mask);    
    }
  }
  long long int sum{0};
  for (auto & cell : memory) sum += cell.second;
  std::cout << sum << '\n';
}

