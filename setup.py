import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ga2",
    version="1.0.0.post1",
    author="Yashas ND",
    author_email="yashasbharadwaj111@gmail.com",
    description="A simple robust Genetic Algorithm utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yashasbharadwaj111/GeneticAlgorithm",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Artificial Life",
        "Intended Audience :: Science/Research",
        "Development Status :: 4 - Beta",
        "Operating System :: POSIX :: Linux",
    ],
)
        
