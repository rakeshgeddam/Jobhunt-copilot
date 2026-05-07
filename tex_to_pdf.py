import subprocess
import os
import argparse
import shutil
import sys

def compile_tex_to_pdf(tex_filepath, engine='pdflatex', clean=True):
    """
    Compiles a .tex file to .pdf using the specified LaTeX engine.
    Ensures consistent formatting and fonts by using the appropriate engine and flags.
    """
    if not os.path.isfile(tex_filepath):
        print(f"Error: The file '{tex_filepath}' does not exist.")
        sys.exit(1)
        
    # Get absolute paths to handle relative path execution
    tex_filepath = os.path.abspath(tex_filepath)
    tex_dir = os.path.dirname(tex_filepath)
    tex_filename = os.path.basename(tex_filepath)
    basename, _ = os.path.splitext(tex_filename)
    
    # Check if the engine is installed
    if not shutil.which(engine):
        print(f"Error: LaTeX engine '{engine}' is not installed or not in PATH.")
        print("Make sure MacTeX or BasicTeX is installed on your system.")
        sys.exit(1)
        
    print(f"Compiling '{tex_filename}' using {engine}...")
    
    # We run the compilation twice to ensure references, page numbers, and formatting are correctly applied
    compile_cmd = [
        engine,
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-output-directory={tex_dir}",
        tex_filepath
    ]
    
    try:
        # First Pass
        print("Pass 1: Generating intermediate files and building document structure...")
        subprocess.run(compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tex_dir)
        
        # Second Pass
        print("Pass 2: Resolving references, styles, and consistent formatting...")
        subprocess.run(compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tex_dir)
        
        print(f"\n✅ Success! PDF generated at: {os.path.join(tex_dir, basename + '.pdf')}")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during compilation. LaTeX output:\n{e.stdout.decode('utf-8', errors='ignore')}")
        print("Please check your .tex file for syntax errors or missing packages.")
        sys.exit(1)
        
    if clean:
        print("\nCleaning up intermediate files (.aux, .log, .out)...")
        extensions_to_clean = ['.aux', '.log', '.out', '.toc', '.fls', '.fdb_latexmk', '.synctex.gz']
        for ext in extensions_to_clean:
            temp_file = os.path.join(tex_dir, basename + ext)
            if os.path.exists(temp_file):
                os.remove(temp_file)
        print("Cleanup complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .tex to .pdf with proper formatting.")
    parser.add_argument("file", help="Path to the .tex file")
    parser.add_argument("--engine", default="pdflatex", choices=["pdflatex", "xelatex", "lualatex"], 
                        help="LaTeX engine to use (pdflatex, xelatex, or lualatex). Use xelatex if you are using custom system fonts.")
    parser.add_argument("--no-clean", action="store_true", help="Do not delete intermediate files (.aux, .log, etc.)")
    
    args = parser.parse_args()
    
    compile_tex_to_pdf(args.file, engine=args.engine, clean=not args.no_clean)
