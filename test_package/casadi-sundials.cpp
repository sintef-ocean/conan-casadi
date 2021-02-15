#include <iostream>
#include <casadi/casadi.hpp>
using namespace casadi;
using namespace std;

// example is taken from casadi/docs/examples/cplusplus/test_linsol.cpp

int main(){

  try {

    SX x = SX::sym("x", 1);
    SX tau = SX::sym("tau", 1);

    SXDict ode_int = {{"x", x}, {"p", tau}, {"ode", -x/tau}};

    auto ode = casadi::integrator(
        "linear", "cvodes", ode_int,
        {{"tf", 1}});

    auto result = ode(DMDict( {{"x0", DM::ones(1,1)}, {"p", 2*DM::ones(1,1)}} ));
    cout << result["xf"] << endl;


  }
  catch(casadi::CasadiException &e){
    cout << e.what() << endl;
    return 1;
  }
  catch(std::exception &e){
    cout << e.what() << endl;
    return 1;
  }
  catch(...){
    cout << "Unknown exception" << endl;
    return 1;
  }
  return 0;
}
