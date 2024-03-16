#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <iomanip>
#include <set>

typedef long long int int36;
typedef std::map<int36, int36> Memory;

int36 ApplyMask(int36 x, const std::string mask) {
  for (int i = 0; i < mask.length(); ++i) {
    int36 m = 1LL << (mask.size() - i - 1);
    switch (mask[i]) {
      case '1': x |= m; break;
      case '0': x &= (~m); break;
      default: break;
    }
  }
  return x;
}

typedef std::set<int36> AddressSet;

AddressSet Apply1Mask(const AddressSet& in, int36 mask) {
  AddressSet out;
  for (int36 address : in) out.insert(address | mask);
  return out;
}

AddressSet ApplyXMask(const AddressSet& in, int36 mask) {
  AddressSet out{Apply1Mask(in, mask)};
  for (int36 address : in) out.insert(address & ~mask);
  return out;
}

AddressSet GenerateAddresses(int36 address, std::string mask) {
  AddressSet out{address};
  for (int i = 0; i < mask.length(); ++i) {
    int36 m = 1LL << (mask.size() - i - 1);
    switch (mask[i]) {
      case '1': out = Apply1Mask(out, m); break;
      case 'X': out = ApplyXMask(out, m); break;
      default: break;
    }
  }
  return out;
}

void Override(Memory& memory, AddressSet addresses, int36 rvalue) {
  for (int36 address : addresses) memory[address] = rvalue;
}


int main() {
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
      int36 idx;
      int36 rvalue;
      is >> rvalue;
      std::stringstream lval{lvalue};
      lval.ignore(10, '['); // Should only be 3 and [.
      lval >> idx;
      AddressSet addresses{GenerateAddresses(idx, mask)};
      Override(memory, addresses, rvalue);
    }
  }
  long long int sum{0};
  for (auto & cell : memory) sum += cell.second;
  std::cout << sum << '\n';
}

