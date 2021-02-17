cmake_minimum_required(VERSION 3.11)

project(TestCasadi
  LANGUAGES CXX
  DESCRIPTION "Test the casadi package")

include("${CMAKE_BINARY_DIR}/conan_paths.cmake")

find_package(casadi CONFIG REQUIRED)

enable_testing()

set(_my_prefix CASADI_CONAN_)
set(CASADI_CONAN_BASIC ON)
set(CASADI_CONAN_SQPMETHOD ON) # Example with built-in plugins of Conic, NLP

list(APPEND _plugins basic sqpmethod)
list(APPEND _plugins csparse lapack mumps hsl)    # LinSol
list(APPEND _plugins osqp qpoases superscs hpmpc) # Conic
list(APPEND _plugins ipopt blocksqp sqpmethod)    # NLP
list(APPEND _plugins sundials)                    # Simulation
list(APPEND _plugins slicot tinyxml)              # Misc
list(APPEND _plugins bonmin cbc clp)              # (MI(N))LP

# TODO: add functional tests for:
# blasfeo is used by hpmpc
# blasfeo, hpmpc, dsdp

macro(casadi_test_add_plugin _plugin)
  string(TOUPPER ${_plugin} _PLUGIN)
  set(_cand ${_my_prefix}${_PLUGIN})
  if(${_cand})
    add_executable(casadi-${_plugin} casadi-${_plugin}.cpp)
    target_link_libraries(casadi-${_plugin} casadi)
    add_test(NAME ${_plugin} COMMAND casadi-${_plugin})
  endif()
endmacro()

foreach(_plugin IN LISTS _plugins)
  casadi_test_add_plugin(${_plugin})
endforeach()
