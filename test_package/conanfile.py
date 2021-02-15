from conans import ConanFile, CMake, tools, RunEnvironment


class CasadiTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake_paths", "cmake", "virtualrunenv")

    _cmake = None

    def _configure_cmake(self):
        if self._cmake is None:
            self._cmake = CMake(self)
            cmake = self._cmake
            # TODO: non-free interfaces
            # ampl, cplex, gurobi, knitro, ooqp, snopt, sqic, worhp
            # TODO: swig_json, swig_matlab, swig_octave, clang_jit
            # TODO: opencl, hpmpc, blasfeo, dsdp(?)

            # LinSol
            cmake.definitions["CASADI_CONAN_CSPARSE"] = self.options["casadi"].csparse
            cmake.definitions["CASADI_CONAN_LAPACK"] = self.options["casadi"].lapack
            cmake.definitions["CASADI_CONAN_MUMPS"] = self.options["casadi"].mumps
            cmake.definitions["CASADI_CONAN_HSL"] = self.options["casadi"].hsl

            # Conic
            cmake.definitions["CASADI_CONAN_HPMPC"] = self.options["casadi"].hpmpc
            cmake.definitions["CASADI_CONAN_OSQP"] = self.options["casadi"].osqp
            cmake.definitions["CASADI_CONAN_QPOASES"] = self.options["casadi"].qpoases
            cmake.definitions["CASADI_CONAN_SUPERSCS"] = self.options["casadi"].superscs

            # NLP
            cmake.definitions["CASADI_CONAN_BLOCKSQP"] = self.options["casadi"].blocksqp
            cmake.definitions["CASADI_CONAN_IPOPT"] = self.options["casadi"].ipopt

            # Integration
            cmake.definitions["CASADI_CONAN_SUNDIALS"] = self.options["casadi"].sundials

            # Other
            cmake.definitions["CASADI_CONAN_SLICOT"] = self.options["casadi"].slicot
            cmake.definitions["CASADI_CONAN_BLASFEO"] = self.options["casadi"].blasfeo
            cmake.definitions["CASADI_CONAN_BONMIN"] = self.options["casadi"].bonmin
            cmake.definitions["CASADI_CONAN_CBC"] = self.options["casadi"].cbc
            cmake.definitions["CASADI_CONAN_CLP"] = self.options["casadi"].clp
            cmake.definitions["CASADI_CONAN_DSDP"] = self.options["casadi"].dsdp
            cmake.definitions["CASADI_CONAN_TINYXML"] = self.options["casadi"].tinyxml
            self._cmake.configure()
        return self._cmake

    def build(self):
        if not tools.cross_building(self.settings):

            cmake = self._configure_cmake()
            cmake.build()

    def test(self):
        if tools.cross_building(self.settings):
            print("NOT RUN (cross-building)")
            return

        # swig_python
        if self.options["casadi"].swig_python:
            self.output.info("Try to load 'casadi' python module")
            try:
                import casadi
                A = casadi.SX.eye(2)
                if casadi.trace(A) == 2:
                    self.output.info("Completed conanized casadi climax")
            except ModuleNotFoundError:
                self.output.error("Unable to load python casadi module")
                exit(1)

        self.output.info("Run consumer tests for library interfaces")
        cmake = self._configure_cmake()

        if self.options["casadi"].hpmpc:
            self.output.warn("HPMPC plugin interface is not tested")
        if self.options["casadi"].dsdp:
            self.output.warn("DSDP interface is not tested(?)")

        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
            cmake.test()

        self.output.info("Casadi OK!")
