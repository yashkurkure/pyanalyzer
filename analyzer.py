import ast
import sys
import os
from collections import defaultdict

def count_loops_and_functions(content):

	tree = ast.parse(content)

	for_count, while_count, user_func_count = 0, 0, 0
	for_loop_lines, while_loop_lines = [], []
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

	FunctionVisitor().visit(tree)

	return for_count, while_count, user_func_count, for_loop_lines, while_loop_lines, user_functions, user_function_calls, unique_non_user_function_calls

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
	[content] = readFile(filepath, readfull=True)

	result = count_loops_and_functions(content)
	for_count, while_count, user_func_count, for_loop_lines, while_loop_lines, user_functions, user_function_calls, unique_non_user_function_calls = result

	print(f"Number of 'for' loops: {for_count}")
	print(f"Number of 'while' loops: {while_count}")
	print(f"Number of user-defined functions: {user_func_count}")
	print(f"Line numbers of 'for' loops: {for_loop_lines}")
	print(f"Line numbers of 'while' loops: {while_loop_lines}")
	print(f"User-defined functions and their line numbers: {dict(user_functions)}")
	print(f"User-defined function calls and their line numbers: {dict(user_function_calls)}")
	print(f"Unique non-user-defined function calls: {unique_non_user_function_calls}")

if __name__ == "__main__":
	main()