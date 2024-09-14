import ast
import os
import networkx as nx
from pyvis.network import Network
import subprocess
import tempfile
import argparse
import webbrowser
import html

def clone_github_repo(repo_url, target_dir):
    try:
        subprocess.run(['git', 'clone', repo_url, target_dir], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Successfully cloned {repo_url}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        raise

def extract_code_snippet(file_path, max_lines=10):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return ''.join(lines[:max_lines]).strip()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return "Unable to read file"

def parse_imports(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
    except SyntaxError:
        print(f"Syntax error in file: {file_path}")
        return []
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append((alias.name, alias.name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append((f"{module}.{alias.name}", alias.name))

    return imports

def build_import_graph(directory):
    graph = nx.DiGraph()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                module_name = os.path.relpath(file_path, directory).replace('.py', '').replace(os.path.sep, '.')
                snippet = extract_code_snippet(file_path)
                
                graph.add_node(module_name, snippet=snippet)

                imports = parse_imports(file_path)
                for full_name, symbol in imports:
                    target_module = full_name.split('.')[0]
                    graph.add_edge(module_name, target_module, symbol=symbol)

    return graph

def visualize_import_graph(graph, output_file):
    net = Network(height="750px", width="100%", directed=True, notebook=False)
    
    # Add nodes
    for node, data in graph.nodes(data=True):
        snippet = html.escape(data.get('snippet', 'No snippet available'))
        net.add_node(node, label=node, title=f"{node}<br><pre>{snippet}</pre>")
    
    # Add edges
    for source, target, data in graph.edges(data=True):
        net.add_edge(source, target, title=data.get('symbol', ''))

    # Set physics layout
    net.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "maxVelocity": 50,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {
          "enabled": true,
          "iterations": 1000,
          "updateInterval": 25
        }
      }
    }
    """)

    # Save and show the graph
    net.save_graph(output_file)
    print(f"Interactive import graph visualization saved as '{output_file}'")
    webbrowser.open(f"file://{os.path.abspath(output_file)}", new=2)

def analyze_codebase(graph):
    print("\nCodebase Analysis:")
    print(f"1. Total number of modules: {graph.number_of_nodes()}")
    print(f"2. Total number of imports: {graph.number_of_edges()}")

    degrees = dict(graph.degree())
    most_imported = max(degrees, key=degrees.get) if degrees else "N/A"
    print(f"3. Most imported module: {most_imported} (imported {degrees.get(most_imported, 0)} times)")

    in_degrees = dict(graph.in_degree())
    most_dependent = max(in_degrees, key=in_degrees.get) if in_degrees else "N/A"
    print(f"4. Module with most dependencies: {most_dependent} ({in_degrees.get(most_dependent, 0)} dependencies)")

    isolated_modules = [node for node, degree in degrees.items() if degree == 0]
    print(f"5. Number of isolated modules: {len(isolated_modules)}")

    if nx.is_directed_acyclic_graph(graph):
        print("6. The codebase has no circular dependencies.")
    else:
        print("6. The codebase contains circular dependencies.")

def main(repo_url, output_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            clone_github_repo(repo_url, temp_dir)
            graph = build_import_graph(temp_dir)
            visualize_import_graph(graph, output_file)
            analyze_codebase(graph)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise  # This will print the full traceback

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an interactive import graph visualization with code snippets for a GitHub repository using Pyvis.")
    parser.add_argument("repo_url", help="URL of the GitHub repository to analyze")
    parser.add_argument("--output", default="import_graph.html", help="Output file name for the visualization (default: import_graph.html)")
    args = parser.parse_args()

    main(args.repo_url, args.output)