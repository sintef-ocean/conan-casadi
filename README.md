[![GCC Conan](https://github.com/sintef-ocean/conan-casadi/workflows/GCC%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-casadi/actions?query=workflow%3A"GCC+Conan")
[![Clang Conan](https://github.com/sintef-ocean/conan-casadi/workflows/Clang%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-casadi/actions?query=workflow%3A"Clang+Conan")
[![MSVC Conan](https://github.com/sintef-ocean/conan-casadi/workflows/MSVC%20Conan/badge.svg)](https://github.com/sintef-ocean/conan-casadi/actions?query=workflow%3A"MSVC+Conan")


[Conan.io](https://conan.io) recipe for [casadi](https://web.casadi.org/).
Most CMake options are exposed as conan options and several of the plugin interface
dependencies are managed with the help of conan packages. The exception is most of the
non-free libraries, see *Known recipe issues* below.

The package is usually consumed using the `conan install` command or a *conanfile.txt*.

## How to use this package

1. Add remote to conan's package [remotes](https://docs.conan.io/en/latest/reference/commands/misc/remote.html?highlight=remotes):

   ```bash
   $ conan remote add sintef https://artifactory.smd.sintef.no/artifactory/api/conan/conan-local
   ```

2. Using *conanfile.txt* in your project with *cmake*

   Add a [*conanfile.txt*](http://docs.conan.io/en/latest/reference/conanfile_txt.html) to your project. This file describes dependencies and your configuration of choice, e.g.:

   ```
   [requires]
   casadi/[>=3.5.5]@sintef/stable

   [options]
   casadi:shared=True
   casadi:lapack=True
   casadi:swig_python=True

   [imports]
   licenses, * -> ./licenses @ folder=True

   [generators]
   virtualenv
   virtualrunenv
   cmake_paths
   cmake_find_package
   ```

   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.13)
   project(TheProject CXX)

   include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
   find_package(casadi CONFIG REQUIRED) # Note: do not use the incomplete MODULE variant

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor casadi::casadi)
   ```
   Then, do
   ```bash
   $ mkdir build && cd build
   $ conan install .. -s build_type=<build_type> --build missing
   ```
   where `<build_type>` is e.g. `Debug` or `Release`.
   You can now continue with the usual dance with cmake commands for configuration and compilation. For details on how to use conan, please consult [Conan.io docs](http://docs.conan.io/en/latest/)

3. Using casadi's python interface

   This recipe enables you to install casadi with desired plugins and use casadi's python
   interface from a virtual environment. Use the same *conanfile.txt* as described above and
   run for instance the following commands:
   ```bash
   $ mkdir casadi_env && cd casadi_env
   $ conan install .. --build missing -o casadi:swig_python=True -o casadi:clp=True
   $ source activate.sh # or on windows: activate.bat
   $ # on windows you may also need: activate_run.bat
   $ python
   ```
   You need to install python dependencies yourself, e.g. `numpy`.

   ```python
   import casadi
   # you can now use casadi's clp interface
   ```

## Package options

  Most options in the `casadi` CMakeLists.txt are exposed as conan options. Many options
  have skipped the `with_` prefix and it should be clear from the context what the option
  implies.

Option | Default | Domain
---|---|---
`copysign_undef`      | False |     [True, False]
`deepbind`            | True  |     [True, False]
`enable_export_all`   | False |     [True, False]
`fPIC`                | True |      [True, False]
`fortran_required`    | False |     [True, False]
`install_internal_headers` | False | [True, False]
`refcount_warnings`   | False |     [True, False]
`shared`              | True  |     [True, False]
`so_version`          | True  |     [True, False]
`thread`              | False |     [True, False]
`thread_mingw`        | False |     [True, False]
`with_common`         | False |     [True, False], not Ipopt on Windows (MSVC)
**Plugin interfaces**
`ampl`                | False |     [True, False]
`blasfeo`             | False |     [True, False]
`blocksqp`            | False |     [True, False]
`bonmin`              | False |     [True, False]
`cbc`                 | False |     [True, False]
`clp`                 | False |     [True, False]
`cplex`               | False |     [True, False]
`csparse`             | True  |     [True, False]
`dsdp`                | False |     [True, False]
`gurobi`              | False |     [True, False]
`hpmpc`               | False |     [True, False]
`hsl`                 | False |     [True, False]
`ipopt`               | False |     [True, False]
`knitro`              | False |     [True, False]
`lapack`              | False |     [True, False], will be enabled if needed, provided by OpenBLAS.
`mumps`               | False |     [True, False]
`ooqp`                | False |     [True, False]
`opencl`              | False |     [True, False]
`openmp`              | False |     [True, False]
`osqp`                | False |     [True, False]
`qpoases`             | False |     [True, False]
`no_qpoases_banner`   | True  |     [True, False]
`slicot`              | False |     [True, False]
`snopt`               | False |     [True, False]
`sqic`                | False |     [True, False]
`sundials`            | True  |     [True, False]
`superscs`            | False |     [True, False]
`tinyxml`             | True  |     [True, False]
`worhp`               | False |     [True, False]
**SWIG interfaces**
`swig_export`         | False |     [True, False]
`swig_import`         | False |     [True, False]
`swig_json`           | False |     [True, False]
`swig_matlab`         | False |     [True, False]
`swig_octave`         | False |     [True, False]
`swig_python`         | True  |     [True, False]
**Developer tools**
`clang_jit`           | False |     [True, False]
`clang_tidy`          | False |     [True, False]
`lint`                | False |     [True, False]
`spell`               | False |     [True, False]
**Compiler settings**
`coverage`            | False |     [True, False]
`dynamic_loading`     | True  |     [True, False]
`extra_checks`        | False |     [True, False]
`extra_warnings`      | False |     [True, False]
`werror`              | False |     [True, False]
**Building external interfaces**
`build_blasfeo`       | True  |     [True, False]
`build_csparse`       | True  |     [True, False]
`build_dsdp`          | False |     [True, False]
`build_hpmpc`         | True  |     [True, False]
`build_sundials`      | True  |     [True, False]
`build_tinyxml`       | True  |     [True, False]
**Other options**
`with_doc`            | False |     [True, False]
`with_examples`       | True  |     [True, False]
`extra_config`        |  |     ANY, key:value,..  comma separated cmake definitions


The `with_common` option enables `lapack`, `qpoases`, `blocksqp`, `superscs`, and `ipopt`,
except on Windows with Visual Studio, where `ipopt` is not currently activated.

## Known recipe issues

  - Several managed dependencies only provide static libraries on Windows (MSVC).
  This does not work well with the dynamic plugin loading system of Casadi.
  As such, some options will not be available on Windows with this recipe.
  - The recipe developer has not managed to compile some dependencies with dynamic libraries on windows.
  - You may want to add the following option `casadi:copysign_undef=True` on windows.
  - To build python interface on Windows, you need debug libraries of python installed.
  - The options have not extensively been tested, and the recipe developer was
  unable to compile several of the optional interfaces on Windows using the Visual Studio
  compiler, including `blasfeo` and `hpmpc`.
  - When a third-party plugin interface is enabled, we assume that its dependency is handled
  by conan, with the exception of `slicot` and those listed below. This may not be the
  desired behaviour, e.g. instead use system-provided packages. In the future we might add
  support for this behavior.
  - Building octave/matlab interfaces requires special effort with respect to swig sources, which will not be handled by this recipe.

  Plugin libraries that are not handled by this recipe are
  - ampl
  - cplex
  - gurobi
  - knitro
  - ooqp
  - snopt
  - sqic
  - worhp
  - octave and matlab interfaces
  - bonmin, but there are plans to add support
