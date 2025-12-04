import sys
import ast

def check_file(filename):
    with open(filename, "r") as f:
        tree = ast.parse(f.read())
    
    errors = []
    for node in ast.walk(tree):
        # 检查是否使用了 print
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
            errors.append(f"Line {node.lineno}: Found usage of 'print()'. Use logger instead.")
        
        # 简单检查 Controller 是否太长 (作为 Fat Controller 的一种启发式检查)
        if "controller" in filename.lower() and isinstance(node, ast.FunctionDef):
            if node.end_lineno - node.lineno > 30:
                errors.append(f"Line {node.lineno}: Controller function '{node.name}' is too long (>30 lines). Move logic to Service.")

    if errors:
        print(f"❌ Style Check Failed for {filename}:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"✅ Style Check Passed for {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_style.py <filename>")
        sys.exit(1)
    check_file(sys.argv[1])