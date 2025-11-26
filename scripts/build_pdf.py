import os
import shutil
import re
import argparse
import subprocess
import sys
import glob

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SOURCE_DIR = os.path.join(PROJECT_ROOT, "contenidos")
TEMP_DIR = os.path.join(PROJECT_ROOT, "contenidos/_build/pdf_temp")
EXPORTS_DIR = os.path.join(PROJECT_ROOT, "contenidos/exports")

def setup_temp_dir():
    """Creates a clean temporary directory and copies content."""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    
    print(f"Copying {SOURCE_DIR} to {TEMP_DIR}...")
    shutil.copytree(SOURCE_DIR, TEMP_DIR, ignore=shutil.ignore_patterns('_build', 'exports'))

def process_file(filepath):
    """Applies regex transformations to a single markdown file using block buffering."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    buffer = []
    in_block = False
    block_type = None # 'admonition', 'dropdown', 'figure', 'other'
    block_header = ""
    block_fence = "" # Store the exact fence string (e.g. "```" or "::::")
    discard_block = False
    
    # Regex patterns
    block_start_pattern = re.compile(r'^(\s*)(`{3,}|:{3,})\{(\w+)\}(.*)$')
    block_end_pattern = re.compile(r'^(\s*)(`{3,}|:{3,})\s*$')
    
    dark_mode_pattern = re.compile(r'class:.*only-dark-mode')

    for line in lines:
        if in_block:
            buffer.append(line)
            
            if dark_mode_pattern.search(line):
                discard_block = True
            
            # Check for end of block
            match_end = block_end_pattern.match(line)
            if match_end:
                closing_fence = match_end.group(2)
                if closing_fence[0] == block_fence[0] and len(closing_fence) >= len(block_fence):
                    # End of block reached. Process buffer.
                    if discard_block:
                        pass 
                    else:
                        if block_type == 'admonition':
                            buffer[0] = buffer[0].replace('{admonition}', '{note}')
                            new_lines.extend(buffer)
                        
                        elif block_type == 'dropdown':
                            match = block_start_pattern.match(block_header)
                            if match:
                                title = match.group(4).strip()
                                indent = match.group(1)
                                new_lines.append(f"{indent}**{title}**\n\n")
                                if len(buffer) > 2:
                                    new_lines.extend(buffer[1:-1])
                            else:
                                new_lines.extend(buffer)

                        else:
                            new_lines.extend(buffer)
                    
                    # Reset state
                    in_block = False
                    buffer = []
                    discard_block = False
                    block_type = None
                    block_fence = ""
            
        else:
            match = block_start_pattern.match(line)
            if match:
                in_block = True
                block_indent = match.group(1)
                block_fence = match.group(2)
                directive = match.group(3)
                block_header = line
                buffer.append(line)
                
                if directive == 'admonition':
                    block_type = 'admonition'
                elif directive == 'dropdown':
                    block_type = 'dropdown'
                else:
                    block_type = 'other'
            else:
                new_lines.append(line)

    if buffer:
        new_lines.extend(buffer)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def process_directory(directory):
    """Recursively processes all .md files in the directory."""
    print(f"Processing markdown files in {directory}...")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file))

def build_typst(target_file=None):
    """Runs the myst build command to generate Typst files."""
    cwd = TEMP_DIR
    # Use --typst instead of --pdf to stop at the intermediate step
    cmd = ["myst", "build", "--execute", "--typst"]
    
    if target_file:
        abs_target = os.path.abspath(target_file)
        if abs_target.startswith(SOURCE_DIR):
            rel_path = os.path.relpath(abs_target, SOURCE_DIR)
        else:
            rel_path = target_file
        cmd.append(rel_path)
    
    print(f"Running build command: {' '.join(cmd)} in {cwd}")
    try:
        subprocess.run(cmd, cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        sys.exit(1)

def post_process_typst():
    """Injects 'Salida:' label before code outputs in generated .typ files."""
    print("Post-processing Typst files...")
    
    # Find the generated typst directory
    # It's usually in _build/temp/mystXXXXXX/
    build_temp_dir = os.path.join(TEMP_DIR, "_build", "temp")
    if not os.path.exists(build_temp_dir):
        print(f"Error: Build temp directory {build_temp_dir} not found.")
        sys.exit(1)

    # Find all .typ files recursively
    typ_files = []
    for root, dirs, files in os.walk(build_temp_dir):
        for file in files:
            if file.endswith(".typ"):
                typ_files.append(os.path.join(root, file))

    # Regex to find code block followed by output block
    # Group 1: Python code block (```python ... ```)
    # Group 2: Whitespace between blocks
    # Group 3: Start of output block (```)
    # We use dotall=True (re.DOTALL) so . matches newlines
    output_pattern = re.compile(r'(```python[\s\S]*?```)(\s+)(```)', re.DOTALL)

    for typ_file in typ_files:
        with open(typ_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if output_pattern.search(content):
            print(f"Injecting 'Salida:' in {typ_file}")
            # Inject #strong("Salida:") before the output block
            # We add a newline after the label just in case
            new_content = output_pattern.sub(r'\1\2#strong("Salida:")\n\3', content)
            
            with open(typ_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

def compile_pdf():
    """Compiles the final PDF using typst."""
    print("Compiling final PDF...")
    
    # Find the main typst file. It's usually apunte-edd.typ (based on export name)
    # We search in the temp dirs
    build_temp_dir = os.path.join(TEMP_DIR, "_build", "temp")
    main_file = None
    
    # Look for apunte-edd.typ
    for root, dirs, files in os.walk(build_temp_dir):
        if "apunte-edd.typ" in files:
            main_file = os.path.join(root, "apunte-edd.typ")
            break
    
    if not main_file:
        print("Error: Main Typst file 'apunte-edd.typ' not found.")
        sys.exit(1)
        
    cmd = ["typst", "compile", main_file]
    print(f"Running: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, cwd=os.path.dirname(main_file), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during Typst compilation: {e}")
        sys.exit(1)
        
    return main_file.replace(".typ", ".pdf")

def move_exports(generated_pdf):
    """Moves generated PDF to the exports directory."""
    dst_pdf = os.path.join(EXPORTS_DIR, "apunte-edd.pdf")
    
    if os.path.exists(generated_pdf):
        print(f"Moving {generated_pdf} to {dst_pdf}")
        os.makedirs(os.path.dirname(dst_pdf), exist_ok=True)
        shutil.copy2(generated_pdf, dst_pdf)
    else:
        print(f"Warning: Expected output file {generated_pdf} not found.")

def main():
    parser = argparse.ArgumentParser(description="Build PDF with pre-processing.")
    parser.add_argument("--chapter", help="Path to a specific chapter/file to build.")
    args = parser.parse_args()

    setup_temp_dir()
    process_directory(TEMP_DIR)
    build_typst(args.chapter)
    post_process_typst()
    generated_pdf = compile_pdf()
    
    if not args.chapter:
        move_exports(generated_pdf)

if __name__ == "__main__":
    main()
