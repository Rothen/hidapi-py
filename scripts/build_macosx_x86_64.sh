cmake -S . -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_COMPILER=/usr/bin/clang \
    -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
    -DHIDAPI_ROOT="$(brew --prefix hidapi)"

cmake --build build --config Release --clean-first --target hidapi-py