from setuptools import setup

setup(name="yt_legacy",
      version="1.0",
      description="A yt extension for the Legacy project.",
      author="Britton Smith",
      author_email="brittonsmith@gmail.com",
      license="BSD",
      url="https://github.com/brittonsmith/yt_legacy",
      packages=["yt_legacy"],
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Environment :: Console",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: BSD License",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: POSIX :: AIX",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python",
          "Topic :: Utilities",
          ],
      install_requires=[
          'yt>=3.5',
      ],
)
