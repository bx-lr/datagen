# Datagen
code to generate a c, c++, clang, gcc, llvm, and cfg dataset

# Project description
This project is to create a data set containing control flow graphs, LLVM IR, and x86 assembly generated from multiple c/c++ files. The code will be emitted with multiple flags enabling compiler permutations of the generated output. Currently, the output is saved off to a csv file with the structure described in the data description section. Code is generated with the help of the godbolt project. More compilers will be added in time.

# Data description

| source_file | compiler | ir | ir_flags | asm | asm_flags |
|   ------   |   ------   |   ------   |   ------   |   ------   |   ------   |
| source file location | compiler used | llvm ir | llvm ir flags | x86 assembly | x86 assembly flags |
||||||

# Why I am interested
I need a high quality c/c++ data set for some other stuff I want to work on. This is the first step in generating that data set.

# Three main points
- I am using a local install of godbolt to perform compilation and more compilers and flags will be added soon
- The input data is in the source directory
- Currently, we emit llvm ir and x86 assembly with clang10

# Prerequisites
This project relies on a local installation of godbolt. It would be a good idea to install it using the documentation provided at https://github.com/compiler-explorer/compiler-explorer. However, this isn't technically necessary as you can point the script at https://godbolt.org/. If you wish to install all of the compilers then you should have a LOT of disk space. Initial testing showed > 100gb of disk space required for a local install with all compilers.


# Further areas of improvement
- Add more compilers
- Add compiler flags
- Add more c code

# Installation and use
- use a virtual environment
```bash
python -m pip install -r requirements.txt
py .\gen_data.py -a http://localhost:10240/ -o data.csv
```

# Resources
https://godbolt.org/
https://github.com/compiler-explorer/compiler-explorer
https://github.com/compiler-explorer/compiler-explorer/blob/main/docs/API.md
https://github.com/compiler-explorer/infra
https://clang.llvm.org/docs/ClangCommandLineReference.html
https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html
