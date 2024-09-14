# Interactive Python Import Graph Visualization with Cohere API

This Python script generates an interactive graph visualization of a Python codebase's import structure. It clones a GitHub repository, builds an import dependency graph, and uses the **Cohere API** to generate brief descriptions for each module's code. The graph can be viewed in a browser, where you can hover over each module node to see the corresponding code snippet and description.

## Features

- **GitHub Repo Cloning**: Automatically clones a GitHub repository for analysis.
- **Import Graph Creation**: Builds a directed graph of the import relationships between Python modules in the codebase.
- **Cohere API Integration**: Extracts and summarizes code from each Python module, providing a brief description using Cohere's language model.
- **Interactive Visualization**: Visualizes the import graph in a browser, where each node displays the module's name, code snippet, and description on hover.
- **Codebase Analysis**: Analyzes the codebase to provide insights such as the most imported module, isolated modules, and circular dependencies.

## Requirements

- **Python 3.x**
- **Cohere API Key**
- The following Python packages:
  - `networkx`
  - `pyvis`
  - `cohere`
  - `argparse`
  - `subprocess`
  - `ast`
  - `webbrowser`
  - `html`

## Installation

1. python .\codeGen_challenge.py your_github_repo

![image](https://github.com/user-attachments/assets/2e71fbce-3ce6-4734-9267-9228aba1ff56)

