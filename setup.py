from setuptools import setup, find_packages
import os

# Utility function to read the requirements.txt file


def read_requirements():
    requirements_path = "requirements.txt"
    if os.path.isfile(requirements_path):
        with open(requirements_path) as req:
            return req.read().splitlines()
    return []


setup(
    name="ai_code_refinement",
    version="0.0.3",
    description="AI Code Refinement",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TeraTheDataConsultant/ai_code_refinement",
    author="Tera Earlywine",
    author_email="tera.earlywine@qbizinc.com",
    # license='MIT',
    packages=find_packages(where='core'),
    package_dir={'': 'core'},
    install_requires=read_requirements(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            # command=folder.script_name:main   # example
            "tdc=cli.cli:main",               # tdc refine --env='staging' --file='test.py'
        ],
    },
    include_package_data=True,
    zip_safe=False,
)