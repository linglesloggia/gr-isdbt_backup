#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-isdbt" for configuration "Debug"
set_property(TARGET gnuradio::gnuradio-isdbt APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(gnuradio::gnuradio-isdbt PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libgnuradio-isdbt.so.cfefc8ed"
  IMPORTED_SONAME_DEBUG "libgnuradio-isdbt.so.1.0.0git"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-isdbt )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-isdbt "${_IMPORT_PREFIX}/lib/x86_64-linux-gnu/libgnuradio-isdbt.so.cfefc8ed" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
