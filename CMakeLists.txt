cmake_minimum_required(VERSION 3.17)
project(libusbmuxd C)

set(CMAKE_C_STANDARD 99)

FILE(GLOB_RECURSE header_file_list ${PROJECT_SOURCE_DIR}/include/*.h)
FILE(GLOB_RECURSE c_file_list ${PROJECT_SOURCE_DIR}/src/*.c)

find_package(libplist)
find_package(libimobiledevice-glue)

list(APPEND libimobiledevice_source_files    
    ${c_file_list}
)

add_library(usbmuxd SHARED ${libimobiledevice_source_files})

target_include_directories(usbmuxd
    PUBLIC         
        include                
        src  
        ${CMAKE_SOURCE_DIR}          
)

target_compile_definitions(usbmuxd PUBLIC 
    PACKAGE_VERSION="2.6.0"
    LIBUSBMUXD_BUILD_SHARED_LIBRARY
    # LIBUSBMUXD_STATIC
    # LIBPLIST_STATIC
    # LIMD_GLUE_STATIC       
)

target_link_libraries(usbmuxd PUBLIC 
    libplist::libplist
    libimobiledevice-glue::libimobiledevice-glue
    ws2_32 
)

set_target_properties(usbmuxd PROPERTIES 
    PUBLIC_HEADER "${header_file_list}"
)

install(
    TARGETS usbmuxd
    EXPORT usbmuxd_targets
    PUBLIC_HEADER DESTINATION "include"
    RUNTIME DESTINATION "bin"
    ARCHIVE DESTINATION "lib"
    LIBRARY DESTINATION "lib"
)
