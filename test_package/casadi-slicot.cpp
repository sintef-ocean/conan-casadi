#include <casadi/core/expm.hpp>
#include <casadi/core/dple.hpp>

int main(){
  auto A = casadi::DM::eye(2);
  auto B = expm(A);

  auto V = casadi::DM::eye(2);
  auto C = dplesol(A, V, "slicot");
  return 0;
}
