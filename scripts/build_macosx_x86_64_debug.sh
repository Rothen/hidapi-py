cmake -S . -B build-debug -G Ninja \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_C_COMPILER=/usr/bin/clang \
    -DCMAKE_CXX_COMPILER=/usr/bin/clang++ \
    -DHIDAPI_ROOT="$(brew --prefix hidapi)"

cmake --build build-debug --config Debug --clean-first --target hidapi-py