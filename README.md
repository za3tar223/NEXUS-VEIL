# NEXUS-VEIL Programming Language

**Created by za3tar** | **Revolutionary Programming Language Implementation**

[![GitHub](https://img.shields.io/badge/GitHub-za3tar223/NEXUS--VEIL-blue?style=flat-square&logo=github)](https://github.com/za3tar223/NEXUS-VEIL)
[![Python](https://img.shields.io/badge/Python-3.7+-green?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-orange?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-red?style=flat-square)](https://github.com/za3tar223/NEXUS-VEIL/releases)

---

## Overview

NEXUS-VEIL is a modern, powerful programming language designed and implemented by **za3tar**. It features an advanced syntax, robust runtime environment, and comprehensive toolchain for building sophisticated applications.

### Key Features

- **Modern Syntax**: Clean, intuitive language design with advanced features
- **Powerful Runtime**: Fast and efficient execution environment
- **Type System**: Dynamic typing with built-in type safety
- **Function Programming**: First-class functions and closures
- **Object Orientation**: Classes, interfaces, and inheritance
- **Error Handling**: Comprehensive try-catch exception system
- **Built-in Functions**: Rich standard library of utility functions
- **Interactive REPL**: Interactive development environment
- **Cross-Platform**: Runs on Windows, macOS, and Linux

---

## Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/za3tar223/NEXUS-VEIL.git
cd NEXUS-VEIL

# Make the scripts executable (on Unix systems)
chmod +x nexus_compiler.py nexus_runtime.py

# Optional: Add to PATH for global access
export PATH="$PATH:$(pwd)"
```

### Verify Installation

```bash
# Check compiler
python nexus_compiler.py

# Check runtime (interactive mode)
python nexus_runtime.py
```

---

## Language Syntax & Features

### Variables and Data Types

```nexus
// Variable declarations
var name = "za3tar";
var age = 25;
var isActive = true;
var data = null;

// Constants
const PI = 3.14159;
const VERSION = "1.0.0";
```

### Functions

```nexus
// Function declaration
func greet(name, greeting) {
    return greeting + ", " + name + "!";
}

// Function calls
var message = greet("za3tar", "Hello");
print(message); // Output: Hello, za3tar!
```

### Control Flow

```nexus
// If statements
if (age >= 18) {
    print("Adult");
} elif (age >= 13) {
    print("Teenager");
} else {
    print("Child");
}

// While loops
var i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}

// For loops
for (var j = 0; j < 10; j = j + 1) {
    if (j == 5) continue;
    if (j == 8) break;
    print(j);
}
```

---

## Usage

### Command Line Interface

#### Compiling NEXUS-VEIL Files

```bash
# Compile a .nv file to AST
python nexus_compiler.py program.nv [output.nvast]

# Examples
python nexus_compiler.py examples/hello_world.nv
```

#### Running NEXUS-VEIL Programs

```bash
# Run source file directly
python nexus_runtime.py program.nv

# Run compiled AST file
python nexus_runtime.py program.nvast

# Interactive REPL mode
python nexus_runtime.py
```

### Interactive REPL

```bash
$ python nexus_runtime.py
NEXUS-VEIL Interactive Runtime v1.0.0 - Created by za3tar
Repository: https://github.com/za3tar223/NEXUS-VEIL
Type 'exit' or 'quit' to exit.

nexus> var x = 10;
nexus> var y = 20;
nexus> print(x + y);
30
nexus> func square(n) { return n * n; }
nexus> square(5);
25
nexus> exit
```

---

## Examples

### Hello World

```nexus
// Hello World in NEXUS-VEIL
func main() {
    print("Hello, NEXUS-VEIL World!");
    print("Language created by za3tar");
    
    var language = "NEXUS-VEIL";
    var creator = "za3tar";
    
    print("Welcome to " + language + " programming!");
    print("Developed by: " + creator);
}

main();
```

### Calculator Example

```nexus
func add(a, b) { return a + b; }
func subtract(a, b) { return a - b; }
func multiply(a, b) { return a * b; }
func divide(a, b) {
    if (b == 0) {
        print("Error: Division by zero!");
        return null;
    }
    return a / b;
}

// Example usage
var result1 = add(10, 5);
var result2 = multiply(7, 8);
var result3 = divide(20, 4);

print("10 + 5 = " + str(result1));
print("7 * 8 = " + str(result2));
print("20 / 4 = " + str(result3));
```

---

## Built-in Functions

NEXUS-VEIL comes with a comprehensive set of built-in functions:

### I/O Functions
- `print(...)` - Print values to console
- `input(prompt)` - Read user input

### Type Functions
- `type(value)` - Get type of value
- `str(value)` - Convert to string
- `num(value)` - Convert to number

### Utility Functions
- `len(collection)` - Get length of string or array

---

## Architecture

### Compiler Architecture

1. **Lexical Analysis** (`NexusLexer`) - Tokenizes source code
2. **Syntax Analysis** (`NexusParser`) - Builds Abstract Syntax Tree (AST)
3. **Code Generation** (`NexusCompiler`) - Generates executable AST

### Runtime Architecture

1. **Execution Engine** (`NexusInterpreter`) - Tree-walking interpreter
2. **Environment System** (`NexusEnvironment`) - Variable scoping
3. **Value System** (`NexusValue`) - Unified value representation

---

## License

NEXUS-VEIL is released under the MIT License.

```
MIT License

Copyright (c) 2025 za3tar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Support & Contact

- **Creator**: za3tar
- **Repository**: [github.com/za3tar223/NEXUS-VEIL](https://github.com/za3tar223/NEXUS-VEIL)
- **Issues**: [Report bugs and feature requests](https://github.com/za3tar223/NEXUS-VEIL/issues)

---

**NEXUS-VEIL** - *Revolutionary Programming Language by za3tar*

*"Bridging the gap between simplicity and power in programming languages."*
