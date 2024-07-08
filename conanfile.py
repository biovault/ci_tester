from conan import ConanFile
from conan.tools.system import package_manager
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.apple import is_apple_os
from pathlib import Path
import subprocess
import platform

class CrossOmp(ConanFile):

    name = "cross"
    version = "0.1"

    # Optional metadata
    description = "Text cross compiling on macos arm to x86_64"
    license = "Apache-2.0"
    url = "https://github.com/biovault/ci_tester.git"

    # Binary config
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps"

    # Sources
    exports_sources = "CMakeLists.txt", "src/*"

    # Build context info
    arch = str(platform.machine())

    if arch == "arm64":
        brew = "/opt/homebrew/bin/brew" 
    else:
        brew = "/usr/local/bin/brew"
    
    def layout(self):
        cmake_layout(self)

    def generate(self):
        if is_apple_os(self):
            generator = "Xcode"

        tc = CMakeToolchain(self, generator=generator)
        if is_apple_os(self):
            print(f"Macos with architecture {self.arch}")
 
            # We can build Universal or per arch on Apple
            if "x86_64" in self.settings.arch and "armv8" in self.settings.arch:
                tc.variables["BUILD_MACOS_UNIVERSAL"] = " ON"
                tc.variables["OpenMP_ROOT"] = str(Path(Path.home(), "libomp").as_posix())
            else:
                proc = subprocess.run(
                    f"{self.brew} --prefix libomp", shell=True, capture_output=True
                )
                prefix_path = f"{proc.stdout.decode('UTF-8').strip()}"
                # essential for find_package on macos
                print(f"Macos OpenMP found at {prefix_path}")
                tc.variables["OpenMP_ROOT"] = prefix_path  
        tc.generate()      

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        install_path = Path(Path.home(), f'build_{self.arch}')
        cmake.install(cli_args=['--prefix', f'{str(install_path)}'])
