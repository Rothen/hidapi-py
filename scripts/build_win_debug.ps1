cmake `
    -S . `
    -B build-debug `
    -G Ninja `
    -DCMAKE_BUILD_TYPE=Debug

cmake --build build-debug --config Release --clean-first --target hidapi-py