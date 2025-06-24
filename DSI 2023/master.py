import subprocess
import time
import os 


def run_r_script(r_file):
    r_reqs = subprocess.run(['Rscript', 'requirements.R'], capture_output=True, text=True)
    if r_reqs.returncode != 0:
        # R requirements installation failed
        error_message = r_reqs.stderr.strip()  # Get the error message
        raise RuntimeError(f"Error installing R requirements: {error_message}")
    result = subprocess.run(['Rscript', r_file], capture_output=True, text=True)
    if result.returncode != 0:
        # R script execution failed
        error_message = result.stderr.strip()  # Get the error message
        raise RuntimeError(f"Error executing R script: {error_message}")



def run_python_script(python_file):
    result = subprocess.run(['python', python_file], capture_output=True, text=True)
    if result.returncode != 0:
        # Python script execution failed
        error_message = result.stderr.strip()  # Get the error message
        raise RuntimeError(f"Error executing Python script: {error_message}")


def install_python_requirements(requirements_file):
    try:
        subprocess.check_call(['pip', 'install', '-r', requirements_file])
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements from {requirements_file}: {e}")
        raise



if __name__ == "__main__":
    start_time = time.time()  # Record the start time
    # Run your R and Python scripts
    r_file = "analysis.R"
    python_file = "figures.py"
    requirements_file = "py_requirements.txt"  # Path to your requirements file
    try:
        print("Running analysis in analysis.R")
        run_r_script(r_file)
        print("R analysis completed --- installing python requirements next")
        install_python_requirements(requirements_file)
        print("python requirements installed --- running figures.py to make figures and tables next")
        run_python_script(python_file)
        print("Python analysis (figures & tables) completed")
    except RuntimeError as e:
        print(e)  # Print the error message
        raise # break 
        # Handle the error or exit the program
        # Example: sys.exit(1) to exit with a non-zero status code
    
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate the total execution time
    print(f"All scripts executed successfully in {execution_time:.2f} seconds.")











