from setuptools import setup, find_packages

setup(
    name="Topsis-Bhavika-102303822",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["pandas", "numpy"],
    entry_points={
        "console_scripts": [
            "topsis=topsis.topsis:main"
        ]
    },
)
