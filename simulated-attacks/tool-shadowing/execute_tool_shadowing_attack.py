import ast
import os

# File paths
base_dir = os.path.dirname(os.path.abspath(__file__))
pre_file = os.path.join(base_dir, "pre_tool_shadowing.py")
post_file = os.path.join(base_dir, "post_tool_shadowing.py")

# Read the content of the files
with open(pre_file, "r") as pre, open(post_file, "r") as post:
    pre_content = pre.read()
    post_content = post.read()

# Parse the files into ASTs
pre_tree = ast.parse(pre_content)
post_tree = ast.parse(post_content)

# Function to merge changes while preserving decorators
def merge_functions(pre_func, post_func):
    # Preserve only @pysealer decorators from pre_func
    post_func.decorator_list = [
        decorator for decorator in pre_func.decorator_list
        if isinstance(decorator, ast.Call) and getattr(decorator.func, 'id', '') == 'pysealer'
    ]

    # Return the merged function
    return post_func

# Find the functions in both files
pre_functions = {node.name: node for node in pre_tree.body if isinstance(node, ast.FunctionDef)}
post_functions = {node.name: node for node in post_tree.body if isinstance(node, ast.FunctionDef)}

# Merge the functions
for func_name, post_func in post_functions.items():
    if func_name in pre_functions:
        pre_func = pre_functions[func_name]
        merged_func = merge_functions(pre_func, post_func)

        # Replace the function in the post_tree
        post_tree.body[post_tree.body.index(post_func)] = merged_func

# Write the merged content back to the post file
with open("merged_tool_shadowing.py", "w") as merged_file:
    merged_file.write(ast.unparse(post_tree))

print("Merged changes while preserving decorators.")

# Update to handle ast.Constant for string constants
# Replace ast.Str with ast.Constant

def is_string_constant(node):
    return isinstance(node, ast.Constant) and isinstance(node.value, str)

# Update the recurse function to use the new check
# Replace all instances of `if isinstance(value, ast.Str):` with `if is_string_constant(value):`