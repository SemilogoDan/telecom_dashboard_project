# Script to filter dependencies
import subprocess

# List of required libraries
required_libraries = ["streamlit", "pandas", "plotly", "scikit-learn", "numpy"]

# Run `pip freeze` and capture the output
result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE, text=True)

# Parse the output and filter only the required libraries
filtered_requirements = []
for line in result.stdout.splitlines():
    for lib in required_libraries:
        if line.startswith(lib):
            filtered_requirements.append(line)
            break

# Write the filtered requirements to `requirements.txt`
with open("requirements.txt", "w") as f:
    f.write("\n".join(filtered_requirements))

print("Filtered requirements saved to requirements.txt")