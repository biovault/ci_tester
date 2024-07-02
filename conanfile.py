from conan import ConanFile
from conan.tools.system import package_manager
from conan.tools.cmake import CMakeToolchain, CMake
from conan.tools.apple import is_apple_os
import subprocess

class CrossOmp(ConanFile):

    name = "cross"
    description = "Text cross compiling on macos arm to x86_64"
    license = "Apache-2.0"
    url = "https://github.com/biovault/ci_tester.git"
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"

    def generate(self):
        if is_apple_os(self):
            generator = "Xcode"

        tc = CMakeToolchain(self, generator=generator)
        if is_apple_os(self):
            proc = subprocess.run(
                "brew --prefix libomp", shell=True, capture_output=True
            )
            prefix_path = f"{proc.stdout.decode('UTF-8').strip()}"
            tc.variables["OpenMP_ROOT"] = prefix_path   
            print(f"libomp path {tc.variables['OpenMP_ROOT']}")   
        tc.generate()      

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()