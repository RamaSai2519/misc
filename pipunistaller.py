import subprocess

installed_packages = subprocess.check_output(["pip", "freeze"]).decode().split("\n")

for package in installed_packages:
    if package:
        package_name = package.split("==")[0]
        subprocess.call(["pip", "uninstall", "-y", package_name])