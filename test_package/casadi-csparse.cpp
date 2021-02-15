#include <iostream>
#include <casadi/casadi.hpp>
using namespace casadi;
using namespace std;
// example is taken from casadi/docs/examples/cplusplus/test_linsol.cpp

int main(){

  try {

    // A
    int ncol = 5, nrow = 5;
    vector<casadi_int> colind = {0, 3, 6, 8, 10, 12};
    vector<casadi_int> row = {0, 1, 4, 1, 2, 4, 0, 2, 0, 3, 3, 4};
    vector<double> nz = {19, 12, 12, 21, 12, 12, 21, 16, 21, 5, 21, 18};
    DM A(Sparsity(nrow, ncol, colind, row), nz);

    // Right hand side
    DM b = DM::ones(ncol);

    DM A_test = A;
    Dict opts;

    Linsol F("F", "csparse", A_test.sparsity(), opts);

    if (F.sfact(A_test.ptr())) casadi_error("'sfact' failed");
    if (F.nfact(A_test.ptr())) casadi_error("'nfact' failed");
    DM x = densify(b);
    if (F.solve(A_test.ptr(), x.ptr(), x.size2())) casadi_error("'solve' failed");

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
