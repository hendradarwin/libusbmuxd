from conan import ConanFile
from conan.tools.cmake import cmake_layout
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps
from conan.tools.files import copy
from os.path import join
from conan.tools.apple import fix_apple_shared_install_name

class libplistConan(ConanFile):
    name = "libusbmuxd"
    version = "2.1.0"
    package_type = "library"


    # Optional metadata
    license = "GNU GENERAL PUBLIC LICENSE"
    author = "Aaron Burghardt"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "A small portable C library to handle Apple Property List files in binary, XML, JSON, or OpenStep format."
    topics = ("ios", "apple", "open source")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}


    
    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
            
    def requirements(self):
        self.requires("libplist/2.6.0")
        self.requires("libimobiledevice-glue/1.3.1")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):        
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        # Make sure the Macros.cmake is packaged
        # copy(self, "*.cmake", src=self.source_folder, dst=self.package_folder)
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        # self.cpp_info.libs = ["libusbmuxd"]
        platform_path = "windows"
        if self.settings.os=="Linux":
            platform_path = "linux"
        
        configuration_path = ""
        if self.settings.build_type == "Debug":
            configuration_path = "debug"
        
        custom_relative_path = join("x64", platform_path, configuration_path)

        lib_path = "lib"
        bin_path = "bin"      
        
        
        self.cpp_info.set_property("cmake_file_name", "libusbmuxd")
        self.cpp_info.set_property("cmake_target_name", "libusbmuxd::libusbmuxd")
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("pkg_config_name", "libusbmuxd")        
        
        self.cpp_info.libdirs = [lib_path]   
        self.cpp_info.libs = ["libusbmuxd"]
        self.cpp_info.bindirs = [bin_path]
        self.cpp_info.components["libusbmuxd"].libs = ["libusbmuxd.a"]
        fix_apple_shared_install_name(self)      
        
