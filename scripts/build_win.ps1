cmake `
    -S . `
    -B build `
    -G Ninja `
    -DCMAKE_BUILD_TYPE=Release

cmake --build build --config Release --clean-first --target hidapi-py