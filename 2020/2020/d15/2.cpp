#include <vector>
#include <iostream>
#include <map>


class Game {
public: 
  Game(std::initializer_list<int> start);
  void Extend();
  void ExtendTo(int n);
  int Last() const {return last;}
  void Print() const;
private:
  std::map<int, int> vals; // Map value to index
  int last;
  int size{0};
};

Game::Game(std::initializer_list<int> start) {
  // We only go to size - 1 as we need to operate on last.
  for (int i{0}; i < start.size() - 1; ++i) 
    vals[*(start.begin() + i)] = i + 1;
  last = *(start.end() - 1);
  size = start.size();
}

void Game::Print() const {
  for (auto p : vals)
    std::cout << p.first << ": " << p.second << '\n';
}

void Game::Extend() {
  // int &lasti{vals[last]};
  if (lasti) {
    last = size - lasti;
  } else {
    last = 0;
  }
  ++size;

}

void Game::ExtendTo(const int n) {
  const int steps = n - vals.size();
  for (int i = 0; i < steps; ++i) Extend();
}


int main() {
  std::map<int, int> pos;
  int last;
  Game game{0, 3, 6};
  // 0
  game.Extend();
  std::cout << game.Last() << '\n';
  // 3
  game.Extend();
  std::cout << game.Last() << '\n';
  //3
  game.Extend();
  std::cout << game.Last() << '\n';
  // 1
  game.Extend();
  std::cout << game.Last() << '\n';
  game.Extend();
  std::cout << game.Last() << '\n';
  // game.ExtendTo(10);
  //std::cout << game.Last() << '\n';
}
