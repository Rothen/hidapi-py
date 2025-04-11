cmake `
    -S . `
    -B build `
    -G Ninja `
    -DCMAKE_BUILD_TYPE=Release `
    -DPYTHON_EXECUTABLE="${env:python_path}\python.exe"

cmake --build build --config Release --clean-first --target hidapi-py