#include <casadi/casadi.hpp>
#include <iostream>
using namespace casadi;

int main(){

  SX x = SX::sym("x", 1);
  SX f = x*x - x;

  SXDict qp = {{"x", x}, {"f", f}, {"g", x}};
  Dict solver_options;
  Function solver = qpsol("solver", "superscs", qp, solver_options);

  DMDict arg = {{"lbx", 0},
                {"ubx", 2},
                {"lbg", 0},
                {"ubg", 2}};
  DMDict res = solver(arg);
  DM x_opt = res["x"];

  std::cout << x_opt << std::endl;

}
