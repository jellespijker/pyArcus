from pathlib import Path

from conan import ConanFile
from conan.tools.env import VirtualRunEnv
from conans import tools
from conans import RunEnvironment


class pyArcusTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "python/3.10.2@python/stable", "pyarcus/5.0.0@ultimaker/testing"
    exports = "test.py"
    generators = "virtualenv_python"

    def generate(self):
        ms = VirtualRunEnv(self)
        ms.generate()

    def test(self):
        v = tools.Version(self.deps_cpp_info["python"].version)
        interp = f"python{v.major}.{v.minor}"
        if self.settings.os == "Windows":
            interp += ".exe"
        interp_path = Path(self.deps_cpp_info["python"].bin_paths[0]).joinpath(interp)
        test_script = Path(__file__).parent.joinpath("test.py")

        with tools.environment_append({"PYTHONPATH": self.deps_env_info["pyarcus"].PYTHONPATH}):
            self.run(f"{interp_path} {test_script}", run_environment = True)
