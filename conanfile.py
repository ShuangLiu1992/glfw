from conan import ConanFile
import conan.tools.files
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.system.package_manager import Apt
import os


class GLFWConan(ConanFile):
    name = "glfw"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def system_requirements(self):
        if self.settings.os == "Linux":
            Apt(self).install(["libxrandr-dev", "libxinerama-dev", "libxcursor-dev", "libxi-dev"])

    def layout(self):
        cmake_layout(self)

    def export_sources(self):
        conan.tools.files.copy(self, "*", self.recipe_folder, self.export_sources_folder)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.presets_prefix = f"{self.settings.os}_{self.settings.build_type}_{self.settings.arch}"
        tc.variables['GLFW_BUILD_EXAMPLES'] = False
        tc.variables['GLFW_BUILD_TESTS'] = False
        tc.variables['GLFW_BUILD_DOCS'] = False
        tc.variables['GLFW_INSTALL'] = True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none")
        self.cpp_info.set_property("cmake_file_name", "glfw3")
        self.cpp_info.set_property("cmake_target_name", "glfw")
        self.cpp_info.builddirs.append(os.path.join("lib", "cmake", "glfw3"))
