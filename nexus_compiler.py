#!/usr/bin/env python3
"""
NEXUS-VEIL Programming Language Compiler
Created by za3tar - Advanced Programming Language Implementation
Repository: https://github.com/za3tar223/NEXUS-VEIL
Watermark: za3tar - Revolutionary Language Design
"""

import re
import sys
import ast
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# za3tar watermark - NEXUS-VEIL Compiler Core
class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"
    
    # Identifiers and Keywords
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    
    # Operators
    ASSIGN = "ASSIGN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    POWER = "POWER"
    
    # Comparison
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    
    # Logical
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    # Delimiters
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    LEFT_BRACKET = "LEFT_BRACKET"
    RIGHT_BRACKET = "RIGHT_BRACKET"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    DOT = "DOT"
    COLON = "COLON"
    
    # Special
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    ARROW = "ARROW"
    DOUBLE_ARROW = "DOUBLE_ARROW"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class NexusLexer:
    """za3tar - NEXUS-VEIL Lexical Analyzer"""
    
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # za3tar Keywords
        self.keywords = {
            'func', 'var', 'const', 'if', 'else', 'elif', 'while', 'for', 'in',
            'return', 'break', 'continue', 'class', 'interface', 'struct',
            'enum', 'import', 'export', 'from', 'as', 'try', 'catch', 'finally',
            'throw', 'async', 'await', 'yield', 'match', 'when', 'default',
            'true', 'false', 'null', 'and', 'or', 'not', 'is', 'in', 'typeof',
            'new', 'delete', 'this', 'super', 'static', 'private', 'public',
            'protected', 'abstract', 'final', 'override', 'virtual'
        }
        
    def current_char(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.position + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def advance(self) -> None:
        if self.position < len(self.source):
            if self.current_char() == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def skip_whitespace(self) -> None:
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self) -> None:
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
        elif self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
        elif self.current_char() == '/' and self.peek_char() == '*':
            self.advance()  # skip /
            self.advance()  # skip *
            while self.current_char():
                if self.current_char() == '*' and self.peek_char() == '/':
                    self.advance()  # skip *
                    self.advance()  # skip /
                    break
                self.advance()
    
    def read_number(self) -> Token:
        start_column = self.column
        num_str = ""
        has_dot = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    break
                has_dot = True
            num_str += self.current_char()
            self.advance()
        
        return Token(TokenType.NUMBER, num_str, self.line, start_column)
    
    def read_string(self, quote: str) -> Token:
        start_column = self.column
        self.advance()  # skip opening quote
        value = ""
        
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()
                escape_char = self.current_char()
                if escape_char == 'n':
                    value += '\n'
                elif escape_char == 't':
                    value += '\t'
                elif escape_char == 'r':
                    value += '\r'
                elif escape_char == '\\':
                    value += '\\'
                elif escape_char == quote:
                    value += quote
                else:
                    value += escape_char if escape_char else ''
                if escape_char:
                    self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() == quote:
            self.advance()  # skip closing quote
        
        return Token(TokenType.STRING, value, self.line, start_column)
    
    def read_identifier(self) -> Token:
        start_column = self.column
        value = ""
        
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() in '_$')):
            value += self.current_char()
            self.advance()
        
        token_type = TokenType.KEYWORD if value in self.keywords else TokenType.IDENTIFIER
        return Token(token_type, value, self.line, start_column)
    
    def tokenize(self) -> List[Token]:
        """za3tar - Main tokenization method"""
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            char = self.current_char()
            
            # Comments
            if char == '#' or (char == '/' and self.peek_char() in ['/', '*']):
                self.skip_comment()
                continue
            
            # Newlines
            if char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line, self.column))
                self.advance()
                continue
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if char in ['"', "'"]:
                self.tokens.append(self.read_string(char))
                continue
            
            # Identifiers and keywords
            if char.isalpha() or char in '_$':
                self.tokens.append(self.read_identifier())
                continue
            
            # Two-character operators
            two_char = char + (self.peek_char() or '')
            if two_char in ['==', '!=', '<=', '>=', '=>', '->', '&&', '||', '**', '//', '++', '--']:
                start_column = self.column
                self.advance()
                self.advance()
                
                token_map = {
                    '==': TokenType.EQUAL,
                    '!=': TokenType.NOT_EQUAL,
                    '<=': TokenType.LESS_EQUAL,
                    '>=': TokenType.GREATER_EQUAL,
                    '=>': TokenType.ARROW,
                    '->': TokenType.ARROW,
                    '&&': TokenType.AND,
                    '||': TokenType.OR,
                    '**': TokenType.POWER,
                    '//': TokenType.DIVIDE,
                }
                
                if two_char in token_map:
                    self.tokens.append(Token(token_map[two_char], two_char, self.line, start_column))
                    continue
            
            # Single-character tokens
            start_column = self.column
            single_char_map = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '=': TokenType.ASSIGN,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATER_THAN,
                '!': TokenType.NOT,
                '(': TokenType.LEFT_PAREN,
                ')': TokenType.RIGHT_PAREN,
                '{': TokenType.LEFT_BRACE,
                '}': TokenType.RIGHT_BRACE,
                '[': TokenType.LEFT_BRACKET,
                ']': TokenType.RIGHT_BRACKET,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
                ':': TokenType.COLON
            }
            
            if char in single_char_map:
                self.tokens.append(Token(single_char_map[char], char, self.line, start_column))
                self.advance()
                continue
            
            # Unknown character
            print(f"Warning: Unknown character '{char}' at line {self.line}, column {self.column}")
            self.advance()
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens

class NexusParser:
    """za3tar - NEXUS-VEIL Syntax Parser"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
    
    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type
    
    def match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        
        current_token = self.peek()
        raise SyntaxError(f"{message} at line {current_token.line}, column {current_token.column}")
    
    def parse(self) -> Dict[str, Any]:
        """za3tar - Main parsing method"""
        statements = []
        
        while not self.is_at_end():
            # Skip newlines
            if self.match(TokenType.NEWLINE):
                continue
                
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return {
            'type': 'Program',
            'body': statements,
            'metadata': {
                'creator': 'za3tar',
                'language': 'NEXUS-VEIL',
                'version': '1.0.0'
            }
        }
    
    def parse_statement(self) -> Optional[Dict[str, Any]]:
        """Parse a statement"""
        try:
            if self.match(TokenType.KEYWORD):
                keyword = self.previous().value
                
                if keyword == 'var':
                    return self.parse_variable_declaration()
                elif keyword == 'func':
                    return self.parse_function_declaration()
                elif keyword == 'if':
                    return self.parse_if_statement()
                elif keyword == 'while':
                    return self.parse_while_statement()
                elif keyword == 'return':
                    return self.parse_return_statement()
            
            # Expression statement
            expr = self.parse_expression()
            self.match(TokenType.SEMICOLON)
            return {
                'type': 'ExpressionStatement',
                'expression': expr
            }
        
        except Exception as e:
            print(f"Parse error: {e}")
            return None
    
    def parse_variable_declaration(self) -> Dict[str, Any]:
        """Parse variable declaration"""
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.parse_expression()
        
        self.match(TokenType.SEMICOLON)
        
        return {
            'type': 'VariableDeclaration',
            'name': name,
            'initializer': initializer
        }
    
    def parse_function_declaration(self) -> Dict[str, Any]:
        """Parse function declaration"""
        name = self.consume(TokenType.IDENTIFIER, "Expected function name").value
        
        self.consume(TokenType.LEFT_PAREN, "Expected '(' after function name")
        
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            parameters.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
            
            while self.match(TokenType.COMMA):
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
        
        self.consume(TokenType.RIGHT_PAREN, "Expected ')' after parameters")
        self.consume(TokenType.LEFT_BRACE, "Expected '{' before function body")
        
        body = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            if self.match(TokenType.NEWLINE):
                continue
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after function body")
        
        return {
            'type': 'FunctionDeclaration',
            'name': name,
            'parameters': parameters,
            'body': body
        }
    
    def parse_expression(self) -> Dict[str, Any]:
        """Parse expression"""
        return self.parse_assignment()
    
    def parse_assignment(self) -> Dict[str, Any]:
        """Parse assignment expression"""
        expr = self.parse_logical_or()
        
        if self.match(TokenType.ASSIGN):
            value = self.parse_assignment()
            return {
                'type': 'AssignmentExpression',
                'left': expr,
                'right': value
            }
        
        return expr
    
    def parse_logical_or(self) -> Dict[str, Any]:
        """Parse logical OR expression"""
        expr = self.parse_logical_and()
        
        while self.match(TokenType.OR):
            operator = self.previous().value
            right = self.parse_logical_and()
            expr = {
                'type': 'BinaryExpression',
                'left': expr,
                'operator': operator,
                'right': right
            }
        
        return expr
    
    def parse_logical_and(self) -> Dict[str, Any]:
        """Parse logical AND expression"""
        expr = self.parse_equality()
        
        while self.match(TokenType.AND):
            operator = self.previous().value
            right = self.parse_equality()
            expr = {
                'type': 'BinaryExpression',
                'left': expr,
                'operator': operator,
                'right': right
            }
        
        return expr
    
    def parse_equality(self) -> Dict[str, Any]:
        """Parse equality expression"""
        expr = self.parse_comparison()
        
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self.previous().value
            right = self.parse_comparison()
            expr = {
                'type': 'BinaryExpression',
                'left': expr,
                'operator': operator,
                'right': right
            }
        
        return expr
    
    def parse_comparison(self) -> Dict[str, Any]:
        """Parse comparison expression"""
        expr = self.parse_term()
        
        while self.match(TokenType.GREATER_THAN, TokenType.GREATER_EQUAL, 
                         TokenType.LESS_THAN, TokenType.LESS_EQUAL):
            operator = self.previous().value
            right = self.parse_term()
            expr = {
                'type': 'BinaryExpression',
                'left': expr,
                'operator': operator,
                'right': right
            }
        
        return expr
    
    def parse_term(self) -> Dict[str, Any]:
        """Parse term expression"""
        expr = self.parse_factor()
        
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous().value
            right = self.parse_factor()
            expr = {
                'type': 'BinaryExpression',
                'left': expr,
                'operator': operator,
                'right': right
            }
        
        return expr
    
    def parse_factor(self) -> Dict[str, Any]:
        """Parse factor expression"""
        expr = self.parse_unary()
        
        while self.match(TokenType.DIVIDE, TokenType.MULTIPLY, TokenType.MODULO):
            operator = self.previous().value
            right = self.parse_unary()
            expr = {
                'type': 'BinaryExpression',
                'left': expr,
                'operator': operator,
                'right': right
            }
        
        return expr
    
    def parse_unary(self) -> Dict[str, Any]:
        """Parse unary expression"""
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.previous().value
            right = self.parse_unary()
            return {
                'type': 'UnaryExpression',
                'operator': operator,
                'operand': right
            }
        
        return self.parse_primary()
    
    def parse_primary(self) -> Dict[str, Any]:
        """Parse primary expression"""
        if self.match(TokenType.KEYWORD):
            value = self.previous().value
            if value in ['true', 'false']:
                return {
                    'type': 'Literal',
                    'value': value == 'true',
                    'raw': value
                }
            elif value == 'null':
                return {
                    'type': 'Literal',
                    'value': None,
                    'raw': 'null'
                }
        
        if self.match(TokenType.NUMBER):
            value = self.previous().value
            return {
                'type': 'Literal',
                'value': float(value) if '.' in value else int(value),
                'raw': value
            }
        
        if self.match(TokenType.STRING):
            return {
                'type': 'Literal',
                'value': self.previous().value,
                'raw': f'"{self.previous().value}"'
            }
        
        if self.match(TokenType.IDENTIFIER):
            return {
                'type': 'Identifier',
                'name': self.previous().value
            }
        
        if self.match(TokenType.LEFT_PAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression")
            return expr
        
        raise SyntaxError(f"Unexpected token {self.peek().value} at line {self.peek().line}")

class NexusCompiler:
    """za3tar - Main NEXUS-VEIL Compiler Class"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.creator = "za3tar"
    
    def compile(self, source_code: str, output_file: Optional[str] = None) -> Dict[str, Any]:
        """Compile NEXUS-VEIL source code"""
        try:
            # Lexical analysis
            lexer = NexusLexer(source_code)
            tokens = lexer.tokenize()
            
            # Syntax analysis
            parser = NexusParser(tokens)
            ast = parser.parse()
            
            # Add compilation metadata
            compilation_result = {
                'ast': ast,
                'tokens': [{
                    'type': token.type.value,
                    'value': token.value,
                    'line': token.line,
                    'column': token.column
                } for token in tokens],
                'metadata': {
                    'compiler_version': self.version,
                    'creator': self.creator,
                    'language': 'NEXUS-VEIL',
                    'compilation_time': str(__import__('datetime').datetime.now()),
                    'source_length': len(source_code)
                }
            }
            
            # Save to file if specified
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(compilation_result, f, indent=2)
            
            return compilation_result
            
        except Exception as e:
            return {
                'error': str(e),
                'metadata': {
                    'compiler_version': self.version,
                    'creator': self.creator,
                    'language': 'NEXUS-VEIL'
                }
            }
    
    def compile_file(self, input_file: str, output_file: Optional[str] = None) -> Dict[str, Any]:
        """Compile NEXUS-VEIL file"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            if not output_file:
                output_file = input_file.replace('.nv', '.nvast')
            
            return self.compile(source_code, output_file)
            
        except FileNotFoundError:
            return {
                'error': f"File not found: {input_file}",
                'metadata': {
                    'compiler_version': self.version,
                    'creator': self.creator
                }
            }
        except Exception as e:
            return {
                'error': str(e),
                'metadata': {
                    'compiler_version': self.version,
                    'creator': self.creator
                }
            }

# za3tar - CLI Interface
def main():
    """za3tar - NEXUS-VEIL Compiler CLI"""
    if len(sys.argv) < 2:
        print("NEXUS-VEIL Compiler v1.0.0 - Created by za3tar")
        print("Usage: python nexus_compiler.py <input_file.nv> [output_file]")
        print("Repository: https://github.com/za3tar223/NEXUS-VEIL")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    compiler = NexusCompiler()
    result = compiler.compile_file(input_file, output_file)
    
    if 'error' in result:
        print(f"Compilation Error: {result['error']}")
        sys.exit(1)
    else:
        print(f"Compilation successful!")
        print(f"AST nodes: {len(result['ast']['body'])}")
        print(f"Tokens: {len(result['tokens'])}")
        print(f"Creator: {result['metadata']['creator']}")

if __name__ == '__main__':
    main()
