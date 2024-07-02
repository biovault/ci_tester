from conan import ConanFile
from conan.tools.system import package_manager
from conan.tools.cmake import CMakeToolchain, CMake
from conan.tools.apple import is_apple_os
import subprocess
import platform

class CrossOmp(ConanFile):

    name = "cross"
    description = "Text cross compiling on macos arm to x86_64"
    license = "Apache-2.0"
    url = "https://github.com/biovault/ci_tester.git"
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"
    arch = str(platform.machine())

    def system_requirements(self):
        if is_apple_os(self):
            proc = subprocess.run(
                f"arch -{self.arch} brew --prefix libomp", shell=True, capture_output=True
            )
            subprocess.run(
                f"ln {proc.stdout.decode('UTF-8').strip()}/lib/libomp.dylib /usr/local/lib/libomp.dylib",
                shell=True,
            )           

    def generate(self):
        if is_apple_os(self):
            generator = "Xcode"

        tc = CMakeToolchain(self, generator=generator)
        if is_apple_os(self):
            print(f"Working with architecture {arch}")
            proc = subprocess.run(
                f"arch -{self.arch} brew --prefix libomp", shell=True, capture_output=True
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