#include <casadi/casadi.hpp>
#include <iostream>
using namespace casadi;

int main(){

  typedef std::vector<double> vdob;
  auto inf = std::numeric_limits<double>::infinity();

  auto A = Sparsity().dense(3,2);

  auto opts = Dict();
  opts["discrete"] = std::vector<bool>{false,false};
  opts["print_time"] = false;

  auto sol_opts = Dict();
  //sol_opts["loglevel"] = 0; // cbc
  opts["clp"] = sol_opts;

  // clp if there are noe discrete
  auto solver = conic("solver", "clp", {{"a", A}}, opts);

  auto g = DM(vdob{3,4});
  auto a = DM(std::vector<vdob>{vdob{1,2},vdob{3,-1},vdob{1,-1}});
  auto lba = DM(vdob{-inf, 0, -inf});
  auto uba = DM(vdob{14, inf, 1.9});

  DMDict prob{{"g", g}, {"a", a}, {"lba", lba}, {"uba", uba}};

  auto sol = solver(prob);

  std::cout << "primal solution " << sol["x"] << std::endl;
  std::cout << "cost " << sol["cost"] << std::endl;

}
