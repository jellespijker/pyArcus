import os

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake
from conan.tools.layout import cmake_layout
from conans import tools

required_conan_version = ">=1.44.1"

class PyArcusConan(ConanFile):
    name = "pyarcus"
    version = "5.0.0"
    license = "LGPL-3.0"
    author = "Ultimaker B.V."
    url = "https://github.com/Ultimaker/pyArcus"
    description = "Communication library between internal components for Ultimaker software"
    topics = ("conan", "python", "binding", "sip", "cura", "protobuf", "c++")
    settings = "os", "compiler", "build_type", "arch"
    revision_mode = "scm"
    build_policy = "missing"
    default_user = "ultimaker"
    default_channel = "testing"
    exports = "LICENSE*"
    # python_requires = ["UltimakerBase/0.1@ultimaker/testing"]  TODO uncomment once it is an actual repo
    # python_requires_extend = "UltimakerBase.UltimakerBase"  TODO uncomment once it is an actual repo
    generators = "sip"
    options = { }
    default_options = { }
    scm = {
        "type": "git",
        "subfolder": ".",
        "url": "auto",
        "revision": "auto"
    }

    @property
    def _base_site_package_path(self):
        return os.path.join("site-packages", "pyArcus")

    def requirements(self):
        self.requires("arcus/5.0.0-a+7924.bce2f4@ultimaker/testing")
        self.requires("protobuf/3.17.1")
        self.requires("python/3.10.2@python/stable")
        self.requires("sip/6.5.0@python/stable")

    def config_options(self):
        if self.settings.os == "Macos":
            self.options["protobuf"].shared = False
        else:
            self.options["protobuf"].shared = True

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, 17)

    def layout(self):
        cmake_layout(self)
        self.cpp.build.libs = ["Arcus"]

    def generate(self):
        cmake = CMakeDeps(self)
        cmake.build_context_activated = ["protobuf"]
        cmake.build_context_build_modules = ["protobuf"]
        cmake.build_context_suffix = {"protobuf": "_BUILD"}
        cmake.build_context_suffix = {"sip": "_BUILD"}
        cmake.generate()

        tc = CMakeToolchain(self)

        # FIXME: This shouldn't be necessary (maybe a bug in Conan????)
        if self.settings.compiler == "Visual Studio":
            tc.blocks["generic_system"].values["generator_platform"] = None
            tc.blocks["generic_system"].values["toolset"] = None

        tc.variables["ALLOW_IN_SOURCE_BUILD"] = True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.so", self._base_site_package_path, keep_path = False)
        self.copy("*.dll", self._base_site_package_path, keep_path = False)
        self.copy("*.dynlib", self._base_site_package_path, keep_path = False)
        self.copy("*.pyi", self._base_site_package_path, keep_path = False)

    def package_info(self):
        if self.in_local_cache:
            self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "site-packages"))
            self.runenv_info.prepend_path("PYTHONPATH", os.path.join(self.package_folder, "site-packages"))
        else:
            # TODO check in editable mode if Python imports correctly
            self.env_info.PYTHONPATH.append(self.build_folder)
            self.runenv_info.prepend_path("PYTHONPATH", self.build_folder)
