# Install script for directory: /home/lingles/fing/gr-isdbt/include/isdbt

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/isdbt" TYPE FILE FILES
    "/home/lingles/fing/gr-isdbt/include/isdbt/api.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/energy_dispersal.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/byte_interleaver.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/carrier_modulation.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/hierarchical_combinator.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/time_interleaver.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/frequency_interleaver.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/time_deinterleaver.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/frequency_deinterleaver.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/symbol_demapper.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/bit_deinterleaver.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/byte_deinterleaver.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/energy_descrambler.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/pilot_signals.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/tmcc_encoder.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/ofdm_synchronization.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/tmcc_decoder.h"
    "/home/lingles/fing/gr-isdbt/include/isdbt/subset_of_carriers.h"
    )
endif()

