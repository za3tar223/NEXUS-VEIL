#!/usr/bin/env python3
"""
NEXUS-VEIL Programming Language Runtime Environment
Created by za3tar - Advanced Runtime Execution Engine
Repository: https://github.com/za3tar223/NEXUS-VEIL
Watermark: za3tar - Revolutionary Runtime Implementation
"""

import json
import sys
import operator
import traceback
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum

# za3tar watermark - NEXUS-VEIL Runtime Core
class NexusValue:
    """za3tar - Base class for all NEXUS-VEIL values"""
    def __init__(self, value: Any, type_name: str):
        self.value = value
        self.type_name = type_name
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"NexusValue({self.value}, {self.type_name})"
    
    def is_truthy(self) -> bool:
        if self.value is None or self.value is False:
            return False
        if isinstance(self.value, (int, float)) and self.value == 0:
            return False
        if isinstance(self.value, str) and self.value == "":
            return False
        if isinstance(self.value, list) and len(self.value) == 0:
            return False
        return True

class NexusEnvironment:
    """za3tar - NEXUS-VEIL Environment for variable scoping"""
    
    def __init__(self, parent: Optional['NexusEnvironment'] = None):
        self.parent = parent
        self.variables: Dict[str, NexusValue] = {}
        self.creator = "za3tar"  # watermark
    
    def define(self, name: str, value: NexusValue) -> None:
        """Define a variable in this environment"""
        self.variables[name] = value
    
    def get(self, name: str) -> NexusValue:
        """Get a variable from this environment or parent environments"""
        if name in self.variables:
            return self.variables[name]
        
        if self.parent:
            return self.parent.get(name)
        
        raise NameError(f"Undefined variable '{name}'")
    
    def assign(self, name: str, value: NexusValue) -> None:
        """Assign a value to an existing variable"""
        if name in self.variables:
            self.variables[name] = value
            return
        
        if self.parent:
            self.parent.assign(name, value)
            return
        
        raise NameError(f"Undefined variable '{name}'")
    
    def has(self, name: str) -> bool:
        """Check if variable exists in this environment or parents"""
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.has(name)
        return False

class NexusFunction:
    """za3tar - NEXUS-VEIL Function representation"""
    
    def __init__(self, name: str, parameters: List[str], body: List[Dict[str, Any]], closure: NexusEnvironment):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure = closure
        self.creator = "za3tar"  # watermark
    
    def arity(self) -> int:
        return len(self.parameters)
    
    def call(self, interpreter: 'NexusInterpreter', arguments: List[NexusValue]) -> NexusValue:
        """Call this function with given arguments"""
        # Create new environment for function execution
        environment = NexusEnvironment(self.closure)
        
        # Bind parameters to arguments
        for i, param in enumerate(self.parameters):
            value = arguments[i] if i < len(arguments) else NexusValue(None, "null")
            environment.define(param, value)
        
        # Execute function body
        try:
            previous_env = interpreter.environment
            interpreter.environment = environment
            
            for statement in self.body:
                interpreter.execute(statement)
            
            # Return null if no explicit return
            return NexusValue(None, "null")
            
        except ReturnValue as return_val:
            return return_val.value
        finally:
            interpreter.environment = previous_env
    
    def __str__(self) -> str:
        return f"<function {self.name}>"

class ReturnValue(Exception):
    """za3tar - Exception for return statements"""
    def __init__(self, value: NexusValue):
        self.value = value
        super().__init__()

class BreakException(Exception):
    """za3tar - Exception for break statements"""
    pass

class ContinueException(Exception):
    """za3tar - Exception for continue statements"""
    pass

class NexusInterpreter:
    """za3tar - Main NEXUS-VEIL Interpreter Class"""
    
    def __init__(self):
        self.globals = NexusEnvironment()
        self.environment = self.globals
        self.version = "1.0.0"
        self.creator = "za3tar"
        
        # Define built-in functions
        self._define_builtins()
    
    def _define_builtins(self):
        """za3tar - Define built-in functions"""
        # Print function
        def builtin_print(args: List[NexusValue]) -> NexusValue:
            output = " ".join(str(arg.value) for arg in args)
            print(output)
            return NexusValue(None, "null")
        
        # Input function
        def builtin_input(args: List[NexusValue]) -> NexusValue:
            prompt = args[0].value if args else ""
            user_input = input(str(prompt))
            return NexusValue(user_input, "string")
        
        # Length function
        def builtin_len(args: List[NexusValue]) -> NexusValue:
            if not args:
                raise ValueError("len() requires at least 1 argument")
            value = args[0].value
            if isinstance(value, (str, list)):
                return NexusValue(len(value), "number")
            raise TypeError(f"len() not supported for {args[0].type_name}")
        
        # Type function
        def builtin_type(args: List[NexusValue]) -> NexusValue:
            if not args:
                raise ValueError("type() requires at least 1 argument")
            return NexusValue(args[0].type_name, "string")
        
        # String conversion
        def builtin_str(args: List[NexusValue]) -> NexusValue:
            if not args:
                return NexusValue("", "string")
            return NexusValue(str(args[0].value), "string")
        
        # Number conversion
        def builtin_num(args: List[NexusValue]) -> NexusValue:
            if not args:
                return NexusValue(0, "number")
            try:
                value = args[0].value
                if isinstance(value, str):
                    return NexusValue(float(value) if '.' in value else int(value), "number")
                return NexusValue(float(value), "number")
            except (ValueError, TypeError):
                raise ValueError(f"Cannot convert {args[0].value} to number")
        
        # Register built-ins
        builtins = {
            'print': builtin_print,
            'input': builtin_input,
            'len': builtin_len,
            'type': builtin_type,
            'str': builtin_str,
            'num': builtin_num
        }
        
        for name, func in builtins.items():
            self.globals.define(name, NexusValue(func, "builtin_function"))
    
    def interpret(self, ast: Dict[str, Any]) -> Any:
        """za3tar - Main interpretation method"""
        try:
            if ast['type'] != 'Program':
                raise ValueError("Invalid AST: Expected Program node")
            
            result = None
            for statement in ast['body']:
                result = self.execute(statement)
            
            return result
            
        except Exception as e:
            print(f"Runtime Error: {e}")
            traceback.print_exc()
            return None
    
    def execute(self, node: Dict[str, Any]) -> Any:
        """Execute a statement node"""
        node_type = node.get('type')
        
        if node_type == 'VariableDeclaration':
            return self.execute_variable_declaration(node)
        elif node_type == 'FunctionDeclaration':
            return self.execute_function_declaration(node)
        elif node_type == 'ExpressionStatement':
            return self.evaluate(node['expression'])
        elif node_type == 'IfStatement':
            return self.execute_if_statement(node)
        elif node_type == 'WhileStatement':
            return self.execute_while_statement(node)
        elif node_type == 'ReturnStatement':
            return self.execute_return_statement(node)
        elif node_type == 'BreakStatement':
            raise BreakException()
        elif node_type == 'ContinueStatement':
            raise ContinueException()
        else:
            raise ValueError(f"Unknown statement type: {node_type}")
    
    def execute_variable_declaration(self, node: Dict[str, Any]) -> None:
        """Execute variable declaration"""
        name = node['name']
        value = NexusValue(None, "null")
        
        if node.get('initializer'):
            value = self.evaluate(node['initializer'])
        
        self.environment.define(name, value)
    
    def execute_function_declaration(self, node: Dict[str, Any]) -> None:
        """Execute function declaration"""
        function = NexusFunction(
            node['name'],
            node['parameters'],
            node['body'],
            self.environment
        )
        
        self.environment.define(node['name'], NexusValue(function, "function"))
    
    def execute_if_statement(self, node: Dict[str, Any]) -> Any:
        """Execute if statement"""
        condition = self.evaluate(node['condition'])
        
        if condition.is_truthy():
            return self.execute(node['then_branch'])
        elif node.get('else_branch'):
            return self.execute(node['else_branch'])
        
        return None
    
    def execute_while_statement(self, node: Dict[str, Any]) -> Any:
        """Execute while statement"""
        try:
            while True:
                condition = self.evaluate(node['condition'])
                if not condition.is_truthy():
                    break
                
                try:
                    self.execute(node['body'])
                except ContinueException:
                    continue
                except BreakException:
                    break
        except BreakException:
            pass
        
        return None
    
    def execute_return_statement(self, node: Dict[str, Any]) -> None:
        """Execute return statement"""
        value = NexusValue(None, "null")
        if node.get('value'):
            value = self.evaluate(node['value'])
        
        raise ReturnValue(value)
    
    def evaluate(self, node: Dict[str, Any]) -> NexusValue:
        """Evaluate an expression node"""
        node_type = node.get('type')
        
        if node_type == 'Literal':
            return self.evaluate_literal(node)
        elif node_type == 'Identifier':
            return self.evaluate_identifier(node)
        elif node_type == 'BinaryExpression':
            return self.evaluate_binary_expression(node)
        elif node_type == 'UnaryExpression':
            return self.evaluate_unary_expression(node)
        elif node_type == 'AssignmentExpression':
            return self.evaluate_assignment_expression(node)
        elif node_type == 'CallExpression':
            return self.evaluate_call_expression(node)
        else:
            raise ValueError(f"Unknown expression type: {node_type}")
    
    def evaluate_literal(self, node: Dict[str, Any]) -> NexusValue:
        """Evaluate literal expression"""
        value = node['value']
        
        if isinstance(value, bool):
            return NexusValue(value, "boolean")
        elif isinstance(value, (int, float)):
            return NexusValue(value, "number")
        elif isinstance(value, str):
            return NexusValue(value, "string")
        elif value is None:
            return NexusValue(None, "null")
        else:
            return NexusValue(value, "unknown")
    
    def evaluate_identifier(self, node: Dict[str, Any]) -> NexusValue:
        """Evaluate identifier expression"""
        return self.environment.get(node['name'])
    
    def evaluate_binary_expression(self, node: Dict[str, Any]) -> NexusValue:
        """Evaluate binary expression"""
        left = self.evaluate(node['left'])
        right = self.evaluate(node['right'])
        operator_str = node['operator']
        
        # Arithmetic operators
        if operator_str == '+':
            if left.type_name == "string" or right.type_name == "string":
                return NexusValue(str(left.value) + str(right.value), "string")
            return NexusValue(left.value + right.value, "number")
        
        elif operator_str == '-':
            return NexusValue(left.value - right.value, "number")
        
        elif operator_str == '*':
            return NexusValue(left.value * right.value, "number")
        
        elif operator_str == '/':
            if right.value == 0:
                raise ZeroDivisionError("Division by zero")
            return NexusValue(left.value / right.value, "number")
        
        elif operator_str == '%':
            return NexusValue(left.value % right.value, "number")
        
        elif operator_str == '**':
            return NexusValue(left.value ** right.value, "number")
        
        # Comparison operators
        elif operator_str == '==':
            return NexusValue(left.value == right.value, "boolean")
        
        elif operator_str == '!=':
            return NexusValue(left.value != right.value, "boolean")
        
        elif operator_str == '<':
            return NexusValue(left.value < right.value, "boolean")
        
        elif operator_str == '<=':
            return NexusValue(left.value <= right.value, "boolean")
        
        elif operator_str == '>':
            return NexusValue(left.value > right.value, "boolean")
        
        elif operator_str == '>=':
            return NexusValue(left.value >= right.value, "boolean")
        
        # Logical operators
        elif operator_str in ['and', '&&']:
            return NexusValue(left.is_truthy() and right.is_truthy(), "boolean")
        
        elif operator_str in ['or', '||']:
            return NexusValue(left.is_truthy() or right.is_truthy(), "boolean")
        
        else:
            raise ValueError(f"Unknown binary operator: {operator_str}")
    
    def evaluate_unary_expression(self, node: Dict[str, Any]) -> NexusValue:
        """Evaluate unary expression"""
        operand = self.evaluate(node['operand'])
        operator_str = node['operator']
        
        if operator_str == '-':
            return NexusValue(-operand.value, "number")
        elif operator_str in ['not', '!']:
            return NexusValue(not operand.is_truthy(), "boolean")
        else:
            raise ValueError(f"Unknown unary operator: {operator_str}")
    
    def evaluate_assignment_expression(self, node: Dict[str, Any]) -> NexusValue:
        """Evaluate assignment expression"""
        value = self.evaluate(node['right'])
        
        if node['left']['type'] == 'Identifier':
            name = node['left']['name']
            self.environment.assign(name, value)
            return value
        else:
            raise ValueError("Invalid assignment target")
    
    def evaluate_call_expression(self, node: Dict[str, Any]) -> NexusValue:
        """Evaluate function call expression"""
        callee = self.evaluate(node['callee'])
        
        arguments = []
        for arg_node in node.get('arguments', []):
            arguments.append(self.evaluate(arg_node))
        
        if callee.type_name == "function":
            return callee.value.call(self, arguments)
        elif callee.type_name == "builtin_function":
            return NexusValue(callee.value(arguments), "null")
        else:
            raise TypeError(f"'{callee.type_name}' object is not callable")

class NexusRuntime:
    """za3tar - Main NEXUS-VEIL Runtime Class"""
    
    def __init__(self):
        self.interpreter = NexusInterpreter()
        self.version = "1.0.0"
        self.creator = "za3tar"
    
    def run_ast(self, ast: Dict[str, Any]) -> Any:
        """Run compiled AST"""
        return self.interpreter.interpret(ast)
    
    def run_file(self, ast_file: str) -> Any:
        """Run compiled AST from file"""
        try:
            with open(ast_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'ast' in data:
                return self.run_ast(data['ast'])
            else:
                return self.run_ast(data)
                
        except FileNotFoundError:
            print(f"Error: File not found: {ast_file}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file: {ast_file}")
            return None
        except Exception as e:
            print(f"Runtime error: {e}")
            return None
    
    def run_source(self, source_code: str) -> Any:
        """Compile and run source code directly"""
        from nexus_compiler import NexusCompiler
        
        compiler = NexusCompiler()
        result = compiler.compile(source_code)
        
        if 'error' in result:
            print(f"Compilation error: {result['error']}")
            return None
        
        return self.run_ast(result['ast'])
    
    def interactive_mode(self):
        """za3tar - Interactive REPL mode"""
        print("NEXUS-VEIL Interactive Runtime v1.0.0 - Created by za3tar")
        print("Repository: https://github.com/za3tar223/NEXUS-VEIL")
        print("Type 'exit' or 'quit' to exit.")
        print()
        
        while True:
            try:
                source = input("nexus> ")
                if source.lower() in ['exit', 'quit']:
                    break
                
                if source.strip():
                    result = self.run_source(source)
                    if result is not None:
                        print(result)
                        
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")

# za3tar - CLI Interface
def main():
    """za3tar - NEXUS-VEIL Runtime CLI"""
    if len(sys.argv) < 2:
        # Interactive mode
        runtime = NexusRuntime()
        runtime.interactive_mode()
        return
    
    runtime = NexusRuntime()
    input_file = sys.argv[1]
    
    if input_file.endswith('.nv'):
        # Compile and run source file
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            runtime.run_source(source_code)
        except FileNotFoundError:
            print(f"Error: File not found: {input_file}")
    elif input_file.endswith('.nvast'):
        # Run compiled AST file
        runtime.run_file(input_file)
    else:
        print("Error: Unsupported file type. Use .nv or .nvast files.")

if __name__ == '__main__':
    main()
