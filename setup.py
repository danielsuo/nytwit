from setuptools import setup, find_packages

setup(name="nytwit",
      version="0.0.1",
      description="nytwit",
      url="https://github.com/thelac/nytwit",
      author="The Leather Apron Club",
      license="MIT",
      packages=find_packages(),
      install_requires=[
          "numpy",
          "scipy",
          "jupyter",
          "ipython",
          "flake8",
          "matplotlib",
          "pandas",
          "scikit-learn",
          "click",
          "requests",
          "tqdm",
          "python-twitter",
          "beautifulsoup4",
          "clickutil"
      ])
