#include <casadi/casadi.hpp>

int main(){
  auto A = casadi::SX::eye(2);
  auto B = trace(A);
  auto C = B == casadi::SX(2);
  return !C.is_one();
}
