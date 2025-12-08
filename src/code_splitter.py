"""
AST-based code splitter that splits code at meaningful semantic boundaries.
Handles functions, classes, and modules while preserving context.
"""

import ast
from typing import List, Dict, Any
from pathlib import Path
from dataclasses import dataclass


@dataclass
class CodeChunk:
    """Represents a semantically meaningful chunk of code."""
    content: str
    file_path: str
    chunk_type: str  # 'function', 'class', 'module', 'method', 'whole_file'
    name: str
    start_line: int
    end_line: int
    parent_context: str = ""  # For methods, the class name

    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata for this chunk."""
        return {
            "file_path": self.file_path,
            "chunk_type": self.chunk_type,
            "name": self.name,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "parent_context": self.parent_context,
            "size": len(self.content),
            "content": self.content  # Store actual code content
        }


class ASTCodeSplitter:
    """Splits code into meaningful chunks using AST parsing."""

    def __init__(self, small_file_threshold: int = 1000):
        """
        Initialize the code splitter.

        Args:
            small_file_threshold: Files under this size (in characters) stay whole
        """
        self.small_file_threshold = small_file_threshold

    def split_python_file(self, file_path: str) -> List[CodeChunk]:
        """
        Split a Python file into semantic chunks.

        Args:
            file_path: Path to the Python file

        Returns:
            List of CodeChunk objects
        """
        file_path_obj = Path(file_path)

        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        # If file is small, keep it whole
        if len(source_code) < self.small_file_threshold:
            return [CodeChunk(
                content=source_code,
                file_path=file_path,
                chunk_type='whole_file',
                name=file_path_obj.name,
                start_line=1,
                end_line=source_code.count('\n') + 1
            )]

        # Parse the file
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            # If parsing fails, return the whole file as one chunk
            return [CodeChunk(
                content=source_code,
                file_path=file_path,
                chunk_type='whole_file',
                name=file_path_obj.name,
                start_line=1,
                end_line=source_code.count('\n') + 1
            )]

        chunks = []
        source_lines = source_code.split('\n')

        # Extract top-level definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                chunks.extend(self._extract_function(node, source_lines, file_path))
            elif isinstance(node, ast.ClassDef):
                chunks.extend(self._extract_class(node, source_lines, file_path))

        # If no chunks were extracted, return the whole file
        if not chunks:
            return [CodeChunk(
                content=source_code,
                file_path=file_path,
                chunk_type='whole_file',
                name=file_path_obj.name,
                start_line=1,
                end_line=len(source_lines)
            )]

        return chunks

    def _extract_function(
        self,
        node: ast.FunctionDef,
        source_lines: List[str],
        file_path: str,
        parent_class: str = ""
    ) -> List[CodeChunk]:
        """Extract a function as a code chunk."""
        start_line = node.lineno
        end_line = node.end_lineno or start_line

        # Get the function content with proper indentation
        content = '\n'.join(source_lines[start_line - 1:end_line])

        chunk_type = 'method' if parent_class else 'function'

        return [CodeChunk(
            content=content,
            file_path=file_path,
            chunk_type=chunk_type,
            name=node.name,
            start_line=start_line,
            end_line=end_line,
            parent_context=parent_class
        )]

    def _extract_class(
        self,
        node: ast.ClassDef,
        source_lines: List[str],
        file_path: str
    ) -> List[CodeChunk]:
        """Extract a class and its methods as code chunks."""
        chunks = []

        # Extract the whole class first
        start_line = node.lineno
        end_line = node.end_lineno or start_line

        class_content = '\n'.join(source_lines[start_line - 1:end_line])

        chunks.append(CodeChunk(
            content=class_content,
            file_path=file_path,
            chunk_type='class',
            name=node.name,
            start_line=start_line,
            end_line=end_line
        ))

        # Extract methods separately for better granularity
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                chunks.extend(
                    self._extract_function(
                        item,
                        source_lines,
                        file_path,
                        parent_class=node.name
                    )
                )

        return chunks

    def split_directory(self, directory_path: str, pattern: str = "**/*.py") -> List[CodeChunk]:
        """
        Split all Python files in a directory into chunks.

        Args:
            directory_path: Path to the directory
            pattern: Glob pattern for files to process

        Returns:
            List of all CodeChunk objects from all files
        """
        dir_path = Path(directory_path)
        all_chunks = []

        for file_path in dir_path.glob(pattern):
            if file_path.is_file():
                try:
                    chunks = self.split_python_file(str(file_path))
                    all_chunks.extend(chunks)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

        return all_chunks
