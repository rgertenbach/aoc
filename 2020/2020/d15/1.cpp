#include <vector>
#include <iostream>


class Game {
public: 
  Game(std::initializer_list<int> start): vals{start} {};
  void Extend();
  void ExtendTo(int n);
  int Last() const {return vals[vals.size() - 1];}
  const std::vector<int>& All() const {return vals;}
private:
  std::vector<int> vals;
};

void Game::Extend() {
  const int last{vals[vals.size() - 1]};
  for (int i{1}; i < vals.size(); ++i) {
    if (vals[vals.size() - i - 1] == last) {
      vals.push_back(i);
      return;
    }
  }
  vals.push_back(0);
}

void Game::ExtendTo(const int n) {
  const int steps = n - vals.size();
  for (int i = 0; i < steps; ++i) Extend();
}


int main() {
  Game game{0, 6, 1, 7, 2, 19, 20};
  game.ExtendTo(2020);
  std::cout << game.Last() << '\n';
}
