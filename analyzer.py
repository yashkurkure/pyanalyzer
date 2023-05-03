import ast
import sys
import os
from collections import defaultdict

def count_loops_and_functions(pyprogram):
	"""
	Refer: https://stackoverflow.com/questions/1515357/simple-example-of-how-to-use-ast-nodevisitor
	count_loops_and_functions counts the python constructs in the file.

	:param path: a python program in the form of a string.
	:return: counts and metrics about the constructs in the python program
	"""

	tree = ast.parse(pyprogram)

	for_count, while_count, user_func_count, if_count = 0, 0, 0, 0 
	for_loop_lines, while_loop_lines, if_lines = [], [], []
	user_functions, user_function_calls = defaultdict(int), defaultdict(list)
	unique_non_user_function_calls = set()

	class FunctionVisitor(ast.NodeVisitor):
		def visit_FunctionDef(self, node):
			nonlocal user_func_count
			user_func_count += 1
			user_functions[node.name] = node.lineno
			self.generic_visit(node)

		def visit_Call(self, node):
			func = node.func
			if isinstance(func, ast.Name) and func.id in user_functions:
				user_function_calls[func.id].append(node.lineno)
			elif isinstance(func, ast.Attribute):
				unique_non_user_function_calls.add(func.attr)
			self.generic_visit(node)

		def visit_For(self, node):
			nonlocal for_count
			for_count += 1
			for_loop_lines.append(node.lineno)
			self.generic_visit(node)

		def visit_While(self, node):
			nonlocal while_count
			while_count += 1
			while_loop_lines.append(node.lineno)
			self.generic_visit(node)
		
		def visit_If(self, node):
			nonlocal if_count
			if_count += 1
			if_lines.append(node.lineno)
			self.generic_visit(node)

	FunctionVisitor().visit(tree)

	return for_count, while_count, if_count, user_func_count, for_loop_lines, while_loop_lines, if_lines, user_functions, user_function_calls, unique_non_user_function_calls

def readFile(path, readfull = True):
	"""
	readFile() reads the file located at a given path

	:param path: path to file
	:param readfull: optional parameter. If true returns the entire file as a single string, else returns a list of all lines.
	:return: a list of strings
	""" 
	content = []
	with open(path, 'r') as file:
		if readfull:
			content.append(file.read())
		else:
			content = file.readlines()
	return content


def main():

	filepath = ""

	# Parse commandline params
	if (len(sys.argv) != 2):
		print("Usage: python3 analyzer.py [<filepath>]")
		exit(-1)
	else:
		filepath = sys.argv[1]
		if not os.path.isfile(filepath):
			print("Invalid file path.")
			print("Usage: python3 analyzer.py [<filepath>]")
			exit(-1)

	# Get the entire file
	[pyprogram] = readFile(filepath, readfull=True)

	result = count_loops_and_functions(pyprogram)
	for_count, while_count, if_count, user_func_count, for_loop_lines, while_loop_lines, if_lines, user_functions, user_function_calls, unique_non_user_function_calls = result

	print("\nAnalysis Results:\n")
	print(f"1. Number of 'for' loops: {for_count}")
	print(f"   Line numbers of 'for' loops: {for_loop_lines}\n")

	print(f"2. Number of 'while' loops: {while_count}")
	print(f"   Line numbers of 'while' loops: {while_loop_lines}\n")

	print(f"3. Number of 'if' statements: {if_count}")
	print(f"   Line numbers of 'if' statements: {if_lines}\n")

	print(f"4. Number of user-defined functions: {user_func_count}")
	print("   User-defined functions and their line numbers:")
	for func, lineno in user_functions.items():
		print(f"      {func}: {lineno}\n")

	print("5. User-defined function calls and their line numbers:")
	for func, lines in user_function_calls.items():
		print(f"   {func}: {lines}\n")

	print("6. Unique non-user-defined function calls:")
	print(f"   {', '.join(sorted(unique_non_user_function_calls))}\n")


if __name__ == "__main__":
	main()