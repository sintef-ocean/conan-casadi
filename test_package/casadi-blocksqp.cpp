#include <iostream>
#include <casadi/casadi.hpp>
using namespace casadi;

int main(){

  try {
    auto x = SX::sym("x");
    auto y = SX::sym("y");
    SXDict nlp = {{"x", SX::vertcat({x,y})},
                  {"f", sq(1-x)+100*sq(y-sq(x))},
                  {"g", x+y}};
    Dict solver_options;
    solver_options["linsol"] = "ldl";
    auto solver = nlpsol("mysolver", "blocksqp", nlp, solver_options);
    DMDict solver_in;
    solver_in["x0"] = std::vector<double>{0,1};
    solver_in["lbx"] = std::vector<double>{-10,1.2};
    solver_in["ubx"] = std::vector<double>{10,2};
    solver_in["lbg"] = -10;
    solver_in["ubg"] = 10;
    auto solver_out = solver(solver_in);
  }
  catch(casadi::CasadiException &e){
    std::cout << e.what() << std::endl;
    return 1;
  }
  return 0;
}
