import subprocess

# Get the list of installed packages
installed_packages = subprocess.check_output(["pip", "freeze"]).decode().split("\n")

# Uninstall each package
for package in installed_packages:
    if package:  # Ignore empty lines
        package_name = package.split("==")[0]
        subprocess.call(["pip", "uninstall", "-y", package_name])