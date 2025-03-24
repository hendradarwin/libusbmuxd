cmake_minimum_required(VERSION 3.17)
project(libusbmuxd C)

set(CMAKE_C_STANDARD 99)

# list(APPEND CMAKE_CXX_SOURCE_FILE_EXTENSIONS c)

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
)

target_link_libraries(usbmuxd PUBLIC 
    libplist::libplist
    libimobiledevice-glue::libimobiledevice-glue
    ole32 
    ws2_32 
    gdi32 
    Iphlpapi)

set_target_properties(usbmuxd PROPERTIES 
    PUBLIC_HEADER "${header_file_list}"
)

install(
    TARGETS usbmuxd
    EXPORT plist_targets
    PUBLIC_HEADER DESTINATION "include/libusbmuxd"
    RUNTIME DESTINATION "bin/x64/$<$<PLATFORM_ID:Windows>:windows>$<$<PLATFORM_ID:Linux>:linux>$<$<CONFIG:Debug,DebugASan,DebugTSan>:/debug>"
    ARCHIVE DESTINATION "lib/x64/$<$<PLATFORM_ID:Windows>:windows>$<$<PLATFORM_ID:Linux>:linux>$<$<CONFIG:Debug,DebugASan,DebugTSan>:/debug>"
    LIBRARY DESTINATION "lib/x64/$<$<PLATFORM_ID:Windows>:windows>$<$<PLATFORM_ID:Linux>:linux>$<$<CONFIG:Debug,DebugASan,DebugTSan>:/debug>"
)

