from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
from conans.tools import os_info
import os


class CasadiConan(ConanFile):
    name = "casadi"
    version = "3.5.5"
    license = "LGPL-3.0"
    url = "https://github.com/casadi/casadi"
    homepage = "https://web.casadi.org/"
    description = \
        "CasADi is an open-source tool for nonlinear "\
        "optimization and algorithmic differentiation."
    topics = ("casadi", "Nonlinear optimization", "Algorithmic differentiation")
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake_find_package", "pkg_config")
    exports = "LICENSE.txt"

    _cmake = None
    _swig = False

    options = {
        "copysign_undef":           [True, False],
        "deepbind":                 [True, False],
        "enable_export_all":        [True, False],
        "fPIC":                     [True, False],
        "fortran_required":         [True, False],
        "install_internal_headers": [True, False],
        "refcount_warnings":        [True, False],
        "shared":                   [True, False],
        "so_version":               [True, False],
        "thread":                   [True, False],
        "thread_mingw":             [True, False],

        "ampl":                     [True, False],
        "blasfeo":                  [True, False],
        "blocksqp":                 [True, False],
        "bonmin":                   [True, False],
        "cbc":                      [True, False],
        "clp":                      [True, False],
        "cplex":                    [True, False],
        "csparse":                  [True, False],
        "dsdp":                     [True, False],
        "gurobi":                   [True, False],
        "hpmpc":                    [True, False],
        "hsl":                      [True, False],
        "ipopt":                    [True, False],
        "knitro":                   [True, False],
        "lapack":                   [True, False],
        "mumps":                    [True, False],
        "ooqp":                     [True, False],
        "opencl":                   [True, False],
        "openmp":                   [True, False],
        "osqp":                     [True, False],
        "qpoases":                  [True, False],
        "no_qpoases_banner":        [True, False],
        "slicot":                   [True, False],
        "snopt":                    [True, False],
        "sqic":                     [True, False],
        "sundials":                 [True, False],
        "superscs":                 [True, False],
        "tinyxml":                  [True, False],
        "worhp":                    [True, False],

        "swig_export":              [True, False],
        "swig_import":              [True, False],
        "swig_json":                [True, False],
        "swig_matlab":              [True, False],
        "swig_octave":              [True, False],
        "swig_python":              [True, False],

        "clang_jit":                [True, False],
        "clang_tidy":               [True, False],
        "lint":                     [True, False],
        "spell":                    [True, False],

        "coverage":                 [True, False],
        "dynamic_loading":          [True, False],
        "extra_checks":             [True, False],
        "extra_warnings":           [True, False],
        "werror":                   [True, False],

        "build_blasfeo":            [True, False],
        "build_csparse":            [True, False],
        "build_dsdp":               [True, False],
        "build_hpmpc":              [True, False],
        "build_sundials":           [True, False],
        "build_tinyxml":            [True, False],

        "with_doc":                 [True, False],
        "with_examples":            [True, False],
        "extra_config": "ANY"

    }

    default_options = (
        "copysign_undef=False",
        "deepbind=True",
        "enable_export_all=False",
        "fPIC=True",
        "fortran_required=False",
        "install_internal_headers=False",
        "refcount_warnings=False",
        "shared=True",
        "so_version=True",
        "thread=True",             # casadi default: False
        "thread_mingw=False",      # window stuff?

        "ampl=False",
        "blasfeo=True",            # casadi default: False
        "blocksqp=True",           # casadi default: False
        "bonmin=False",     # T
        "cbc=True",                # casadi default: False
        "clp=True",                # casadi default: False
        "cplex=False",
        "csparse=True",
        "dsdp=True",               # casadi default: False
        "gurobi=False",
        "hpmpc=True",
        "hsl=True",                # casadi default: False
        "ipopt=True",              # casadi default: False
        "knitro=False",
        "lapack=False",  # conditionally on  # default: False
        "mumps=True",              # casadi default: False
        "ooqp=False",
        "opencl=False",
        "openmp=True",
        "osqp=True",               # casadi default: False
        "qpoases=True",            # casadi default: False
        "no_qpoases_banner=True",  # casadi default: False
        "slicot=False",            # casadi default: False, libslicot-dev
        "snopt=False",
        "sqic=False",
        "sundials=True",
        "superscs=True",           # casadi default: False
        "tinyxml=True",
        "worhp=False",

        "swig_export=False",
        "swig_import=False",
        "swig_json=True",
        "swig_matlab=False",
        "swig_octave=False",       # EXPERIMENTAL
        "swig_python=True",        # casadi default: False

        "clang_jit=False",
        "clang_tidy=False",
        "lint=False",
        "spell=False",

        "coverage=False",
        "dynamic_loading=True",
        "extra_checks=False",
        "extra_warnings=False",
        "werror=False",

        "build_blasfeo=True",
        "build_csparse=True",
        "build_dsdp=True",          # casadi default: False
        "build_hpmpc=True",
        "build_sundials=True",
        "build_tinyxml=True",

        "with_doc=False",
        "with_examples=True",
        "extra_config=CPACK_BINARY_DEB:ON"     # key:value,..  comma separated cmake definitions
    )

    def _configure_cmake(self, install_prefix, force=False):
        if self._cmake is None or force:
            self._cmake = CMake(self)
            self._cmake.definitions["CMAKE_INSTALL_PREFIX"] = install_prefix
            self._cmake.definitions["CPACK_PACKAGING_INSTALL_PREFIX"] = install_prefix
            self._cmake.definitions["PYTHON_PREFIX"] = install_prefix

            if self.settings.os != "Windows":
                self._cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC

            self._cmake.definitions["WITH_COPYSIGN_UNDEF"] = self.options.copysign_undef
            self._cmake.definitions["WITH_DEEPBIND"] = self.options.deepbind
            self._cmake.definitions["ENABLE_EXPORT_ALL"] = self.options.enable_export_all
            self._cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
            self._cmake.definitions["FORTRAN_REQUIRED"] = self.options.fortran_required
            self._cmake.definitions["INSTALL_INTERNAL_HEADERS"] = self.options.install_internal_headers
            self._cmake.definitions["WITH_REFCOUNT_WARNINGS"] = self.options.refcount_warnings
            self._cmake.definitions["WITH_SELFCONTAINED"] = True
            if self.options.shared:
                self._cmake.definitions["ENABLE_SHARED"] = True
                self._cmake.definitions["ENABLE_STATIC"] = False
            else:
                self._cmake.definitions["ENABLE_SHARED"] = False
                self._cmake.definitions["ENABLE_STATIC"] = True
            self._cmake.definitions["WITH_SO_VERSION"] = self.options.so_version
            self._cmake.definitions["WITH_THREAD"] = self.options.thread
            self._cmake.definitions["WITH_THREAD_MINGW"] = self.options.thread_mingw

            self._cmake.definitions["WITH_AMPL"] = self.options.ampl
            self._cmake.definitions["WITH_BLASFEO"] = self.options.blasfeo
            self._cmake.definitions["WITH_BLOCKSQP"] = self.options.blocksqp
            self._cmake.definitions["WITH_CBC"] = self.options.cbc
            self._cmake.definitions["WITH_CLP"] = self.options.clp
            self._cmake.definitions["WITH_CPLEX"] = self.options.cplex
            self._cmake.definitions["WITH_CSPARSE"] = self.options.csparse
            self._cmake.definitions["WITH_DSDP"] = self.options.dsdp
            self._cmake.definitions["WITH_GUROBI"] = self.options.gurobi
            self._cmake.definitions["WITH_HPMPC"] = self.options.hpmpc
            self._cmake.definitions["WITH_HSL"] = self.options.hsl
            self._cmake.definitions["WITH_IPOPT"] = self.options.ipopt
            self._cmake.definitions["WITH_KNITRO"] = self.options.knitro
            self._cmake.definitions["WITH_LAPACK"] = self.options.lapack
            self._cmake.definitions["WITH_MUMPS"] = self.options.mumps
            self._cmake.definitions["WITH_OOQP"] = self.options.ooqp
            self._cmake.definitions["WITH_OPENCL"] = self.options.opencl
            self._cmake.definitions["WITH_OPENMP"] = self.options.openmp
            self._cmake.definitions["WITH_OSQP"] = self.options.osqp
            self._cmake.definitions["WITH_QPOASES"] = self.options.qpoases
            self._cmake.definitions["WITH_NO_QPOASES_BANNER"] = self.options.no_qpoases_banner
            self._cmake.definitions["WITH_SLICOT"] = self.options.slicot
            self._cmake.definitions["WITH_SNOPT"] = self.options.snopt
            self._cmake.definitions["WITH_SQIC"] = self.options.sqic
            self._cmake.definitions["WITH_SUNDIALS"] = self.options.sundials
            self._cmake.definitions["WITH_SUPERSCS"] = self.options.superscs
            self._cmake.definitions["WITH_TINYXML"] = self.options.tinyxml
            self._cmake.definitions["WITH_WORHP"] = self.options.worhp
            self._cmake.definitions["SWIG_EXPORT"] = self.options.swig_export
            self._cmake.definitions["SWIG_IMPORT"] = self.options.swig_import
            self._cmake.definitions["WITH_JSON"] = self.options.swig_json
            self._cmake.definitions["WITH_MATLAB"] = self.options.swig_matlab
            self._cmake.definitions["WITH_OCTAVE"] = self.options.swig_octave
            self._cmake.definitions["WITH_PYTHON"] = self.options.swig_python
            self._cmake.definitions["WITH_PYTHON3"] = self.options.swig_python
            self._cmake.definitions["WITH_CLANG"] = self.options.clang_jit # WITH_CLANG
            self._cmake.definitions["WITH_CLANG_TIDY"] = self.options.clang_tidy
            self._cmake.definitions["WITH_LINT"] = self.options.lint
            self._cmake.definitions["WITH_SPELL"] = self.options.spell
            self._cmake.definitions["WITH_COVERAGE"] = self.options.coverage
            self._cmake.definitions["WITH_DL"] = self.options.dynamic_loading
            self._cmake.definitions["WITH_EXTRA_CHECKS"] = self.options.extra_checks
            self._cmake.definitions["WITH_EXTRA_WARNINGS"] = self.options.extra_warnings
            self._cmake.definitions["WITH_WERROR"] = self.options.werror
            self._cmake.definitions["WITH_BUILD_BLASFEO"] = self.options.build_blasfeo
            self._cmake.definitions["WITH_BUILD_CSPARSE"] = self.options.build_csparse
            self._cmake.definitions["WITH_BUILD_DSDP"] = self.options.build_dsdp
            self._cmake.definitions["WITH_BUILD_HPMPC"] = self.options.build_hpmpc
            self._cmake.definitions["WITH_BUILD_SUNDIALS"] = self.options.build_sundials
            self._cmake.definitions["WITH_BUILD_TINYXML"] = self.options.build_tinyxml
            self._cmake.definitions["WITH_DOC"] = self.options.with_doc
            self._cmake.definitions["WITH_EXAMPLES"] = self.options.with_examples

            # use CMAKE_INSTALL_PREFIX over CPACK_PACKAGING_INSTALL_PREFIX
            # since some packagers does not respect the DESTDIR
            self._cmake.definitions["CPACK_SET_DESTDIR"] = True

            extra_config = str(self.options.get_safe('extra_config')).split(',')
            for a_config in extra_config:
                if a_config:
                    key_val = a_config.split(':')
                    if len(key_val) == 2:
                        self._cmake.definitions[key_val[0]] = key_val[1]
                    else:
                        self.output.warn(
                            "casadi:options:extra_config {} unexpected parsing"
                            .format(key_val))

            if self.settings.compiler == 'gcc':
                self._cmake.definitions["CMAKE_CXX_FLAGS"] = '-Wno-psabi'

            if self._swig:
                swiglib = os.path.join(self.deps_env_info["swig"].PATH[0],
                                       "swiglib")
                swigpython = os.path.join(swiglib, "python")
                swigoctave = os.path.join(swiglib, "octave")
                # The order of include seems important.
                self._cmake.definitions["CMAKE_SWIG_FLAGS"] = \
                    "-I{};-I{};-I{};-cpperraswarn".format(
                        swigpython, swigoctave, swiglib)

            self._cmake.configure(source_folder=self.name)
        return self._cmake

    def build_requirements(self):

        if self._swig:
            self.build_requires("swig/[>=4.0.0]")

    def requirements(self):

        if self.options.lapack:
            self.output.info("Use LAPACK provided by OpenBLAS")
            self.requires("openblas/[>=0.3.12]")

        if self.options.ipopt:
            self.requires("ipopt/[>=3.12.0]@kluster/testing")

        if self.options.clp:
            self.output.warn("coin-clp does not currently use optimized BLAS/LAPACK")
            self.requires("coin-clp/[>=1.17.6]")

        if self.options.cbc:
            self.output.warn("coin-cbc does not currently use optimized BLAS/LAPACK")
            self.requires("coin-cbc/[>=2.10.5]")

    def configure(self):

        if self.options.qpoases or self.options.blocksqp or self.options.slicot:
            self.options.lapack = True

        if self.options.blocksqp:
            self.options.qpoases = True

        if self.options.hpmpc:
            self.options.blasfeo = True

        if self.options.sqic or self.options.slicot or self.options.lapack:
            self.options.fortran_required = True

        if self.options.swig_export or self.options.swig_import or \
           self.options.swig_json or self.options.swig_matlab or \
           self.options.swig_octave or self.options.swig_python:
            self._swig = True

        if self.options.clang_jit:
            self.output.warn(
                "'clang_jit': May not work for llvm 10, due to" +
                " API changes(?) of clang::CompilerInvocation::CreateFromArgs")

        if self.options.lapack:
            self.options["openblas"].shared = self.options.shared  # optionally?
            self.options["openblas"].use_thread = self.options.thread
            self.options["openblas"].build_lapack = True
            self.options["openblas"].dynamic_arch = True  # TODO: Should be set optionally?
            if self.settings.os != 'Windows':
                self.options["openblas"].fPIC = self.options.fPIC

        if self.options.slicot and os_info.is_windows:
            raise ConanInvalidConfiguration(
                "option:slicot is not supported on Windows with this recipe")

    def source(self):

        _git = tools.Git(folder=self.name)
        _git.clone("https://github.com/casadi/casadi.git",
                   branch=self.version,
                   shallow=True)

        if self.options.superscs or self.options.osqp or \
           self.options.blasfeo or self.options.hpmpc:
            self.output.info("Running git submodule for blasfeo/hpmpc/osqp/superscs")
            self.run("git submodule update --init --recursive",
                     cwd=os.path.join(self.name, "external_packages"))

        if self.options.swig_export or self.options.swig_import or \
           self.options.swig_json or self.options.swig_matlab or \
           self.options.swig_octave or self.options.swig_python:
            # CMAKE_MODULE_PATH is overwritten several places..
            tools.replace_in_file(
                os.path.join(self.name, "swig", "CMakeLists.txt"),
                "find_package(SWIG REQUIRED)",
                "set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})\n\
  find_package(swig MODULE REQUIRED)\n\
  find_program(SWIG_EXECUTABLE swig)")


        cmakelists = os.path.join(self.name, "CMakeLists.txt")

        tools.replace_in_file(
            cmakelists,
            "# Check if mkstemps is available",
            "set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)\n\
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH})")

        if self.options.lapack:
            # use openblas' bundled lapack
            tools.replace_in_file(
                cmakelists,
                "find_package(LAPACK",
                "find_package(OpenBLAS")
            tools.replace_in_file(
                cmakelists,
                "LAPACK_FOUND", "OpenBLAS_FOUND")
            tools.replace_in_file(
                cmakelists,
                "add_feature_info(lapack",
                "set(LAPACK_LIBRARIES OpenBLAS::OpenBLAS)\n\
add_feature_info(lapack")


        if self.options.clp:
            tools.replace_in_file(
                cmakelists,
                "find_package(CLP REQUIRED)",
                "find_package(coin-clp MODULE REQUIRED)\n\
set(CLP_INCLUDE_DIRS coin-clp_INCLUDE_DIRS)\n\
set(CLP_LIBRARIES coin-clp::coin-clp)")

        if self.options.cbc:
            tools.replace_in_file(
                cmakelists,
                "find_package(CBC REQUIRED)",
                "find_package(coin-cbc MODULE REQUIRED)\n\
set(CBC_INCLUDE_DIRS coin-cbc_INCLUDE_DIRS)\n\
set(CBC_LIBRARIES coin-cbc::coin-cbc)")

        if self.options.hsl:
            tools.replace_in_file(
                cmakelists,
                "find_package(HSL REQUIRED)",
                "find_package(coinhsl MODULE REQUIRED)\n\
set(HSL_LIBRARIES coinhsl::coinhsl)")

        if self.options.mumps:
            tools.replace_in_file(
                os.path.join(self.name, "casadi", "interfaces", "mumps",
                             "mumps_interface.hpp"),
                "mumps_seq/mpi.h",
                "mumps_mpi.h")
            tools.replace_in_file(
                os.path.join(self.name, "casadi", "interfaces", "mumps",
                             "mumps_interface.cpp"),
                "m->id->nnz",
                "m->id->nz")

    def build(self):
        cmake = self._configure_cmake(install_prefix=self.package_folder)
        cmake.build()

    def package(self):
        cmake = self._configure_cmake(install_prefix=self.package_folder)
        cmake.install()

        # remove pkg-config casadi.pc and lib/*.cmake, -> not relocatable
        tools.rmdir(os.path.join(self.package_folder, "casadi", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "lib"))

        self.copy("LICENSE.txt", dst="licenses",
                  ignore_case=True, keep_path=False)

        # Subject to change: build package, but not moved to the package folder
        if False:
            if self.settings.os == "Windows":
                package_prefix = "C:/Program Files/casadi"
            elif self.settings.os == "Linux":
                package_prefix = "/opt"

            cmake = self._configure_cmake(install_prefix=package_prefix,
                                      force=True)
            cmake.build(target='package')

    def package_info(self):
        self.cpp_info.libs = ["casadi"]
        self.cpp_info.includedirs = ["casadi/include"]
        self.cpp_info.libdirs = [self.name]
        #self.cpp_info.builddirs.append(self.name)

        if self.options.osqp:
            self.cpp_info.includedirs.append("casadi/include/osqp")
            self.cpp_info.includedirs.append("casadi/include/qdldl")
            self.cpp_info.libs.append("osqp")
            self.cpp_info.libs.append("qdldl")

        if self.options.swig_python:
            self.env_info.PYTHONPATH.append(self.package_folder)

    def system_requirements(self):

        installer = tools.SystemPackageTool()
        debian_based = (os_info.linux_distro == "ubuntu" or
                        os_info.linux_distro == "debian")

        if self.options.thread:
            if os_info.is_linux and debian_based:
                installer.install("libpthread-stubs0-dev")
            if os_info.is_msys:
                installer = tools.SystemPackageTool(tool=tools.PacManTool())
                installer.install('mingw-w64-x86_64-winpthreads-git')

        # For now: we assume that the fortran compiler is installed
        # TODO: Need a way of handling fortran runtime
        # flang: libflang0d-7 (flang 7)
        # gfortran: libgfortran{3,4,5}: gfortran: {{5,6},7,{8,9,10}}
        if self.options.fortran_required:
            self.output.warn("A fortran compiler is needed.")

        if self.options.slicot:
            if os_info.is_linux and debian_based:
                installer.install("libslicot-dev")
                if self.settings.compiler == "gcc":
                    installer.install("gfortran-{}"
                                      .format(self.settings.compiler.version))
