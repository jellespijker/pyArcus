project(pyArcus)
cmake_minimum_required(VERSION 3.20)

include(cmake/StandardProjectSettings.cmake)

find_package(arcus REQUIRED 5.0.0)

find_package(python REQUIRED)
if(NOT DEFINED Python_VERSION)
    set(Python_VERSION
            3.10
            CACHE STRING "Python Version" FORCE)
    message(STATUS "Setting Python version to ${Python_VERSION}. Set Python_VERSION if you want to compile against an other version.")
endif()
find_package(Python ${Python_VERSION} EXACT REQUIRED COMPONENTS Interpreter Development)
message(STATUS "Linking and building ${project_name} against Python ${Python_VERSION}")

find_package(Protobuf 3.17.1 REQUIRED)
find_package(sip REQUIRED 6.5.0)

add_library(pyArcus INTERFACE)

target_include_directories(pyArcus
        INTERFACE
            $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
            $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include/>
        )

set(SIP_MODULE "${CMAKE_SOURCE_DIR}/pyArcus/pyArcus.sip")
set(EXTRA_SIP_FILES
        "${CMAKE_SOURCE_DIR}/pyArcus/Error.sip"
        "${CMAKE_SOURCE_DIR}/pyArcus/PythonMessage.sip"
        "${CMAKE_SOURCE_DIR}/pyArcus/SocketListener.sip"
        "${CMAKE_SOURCE_DIR}/pyArcus/Types.sip"
        )
set(HDR_FILES "PythonMessage.h")
set(SRC_FILES "${CMAKE_SOURCE_DIR}/src/PythonMessage.cpp")

target_compile_features(pyArcus INTERFACE cxx_std_17)
set_project_warnings(pyArcus)
target_link_libraries(pyArcus INTERFACE arcus::arcus protobuf::protobuf Python::Python)

add_sip_module(pyArcus ${SIP_MODULE} "${EXTRA_SIP_FILES}" "${HDR_FILES}" "${SRC_FILES}")