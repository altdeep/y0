<p align="center">
  <img src="docs/source/logo.png" height="120">
</p>

<h1 align="center">
  y0
</h1>

<p align="center">
    <a href="https://github.com/altdeep/y0/actions?query=workflow%3ATests">
        <img alt="Tests" src="https://github.com/altdeep/y0/workflows/Tests/badge.svg" />
    </a>
   <a href="https://github.com/cthoyt/cookiecutter-python-package">
      <img alt="Cookiecutter template from @cthoyt" src="https://img.shields.io/badge/Cookiecutter-python--package-yellow" /> 
   </a>
    <a href="https://pypi.org/project/y0">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/y0" />
    </a>
    <a href="https://pypi.org/project/y0">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/y0" />
    </a>
    <a href="https://github.com/altdeep/y0/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/y0" />
    </a>
    <a href='https://y0.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/y0/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href="https://zenodo.org/badge/latestdoi/328745468">
        <img src="https://zenodo.org/badge/328745468.svg" alt="DOI">
    </a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" />
    </a>
</p>

`y0` (pronounced "why not?") is Python code for causal inferencing.

This is a fork of the [y0 package](https://github.com/y0-causal-inference/y0).
The goal of the fork is to have a fixed codebase for reference by a printed
book.  If you are interested in y0, you are encouraged to visit the original
repository. 

## 💪 Getting Started

See the notebooks in the notebooks directory to get started.

## ⬇️ Installation

Install directly from GitHub with:

```bash
$ pip install git+https://github.com/altdeep/y0.git
```

To install in development mode, use the following:

```bash
$ git clone git+https://github.com/altdeep/y0.git
$ cd y0
$ pip install -e .
```

## ⚖️ License

The code in this package is licensed under the [BSD-3-Clause
license](https://github.com/altdeep/y0/blob/master/LICENSE).

## 🙏 Contributing

Contributions are appreciated, especially if there are errors relevant to books,
courses, or other pedagogical materials. But for developing the ideas in this
repo, you are encouraged to contribute to the [original repo](https://github.com/y0-causal-inference/y0)

### 🍪 Cookiecutter

This package was created with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-python-package](https://github.com/cthoyt/cookiecutter-python-package) template.

### ❓ Testing

After cloning the repository and installing `tox` with `pip install tox`, the unit tests in the `tests/` folder can be
run reproducibly with:

```shell
$ tox
```

Additionally, these tests are automatically re-run with each commit in a [GitHub Action](https://github.com/altdeep/y0/actions?query=workflow%3ATests).

### 📦 Making a Release

After installing the package in development mode and installing
`tox` with `pip install tox`, the commands for making a new release are contained within the `finish` environment
in `tox.ini`. Run the following from the shell:

```shell
$ tox -e finish
```

This script does the following:

1. Uses BumpVersion to switch the version number in the `setup.cfg` and
   `src/y0/version.py` to not have the `-dev` suffix
2. Packages the code in both a tar archive and a wheel
3. Uploads to PyPI using `twine`. Be sure to have a `.pypirc` file configured to avoid the need for manual input at this
   step
4. Push to GitHub. You'll need to make a release going with the commit where the version was bumped.
5. Bump the version to the next patch. If you made big changes and want to bump the version by minor, you can
   use `tox -e bumpversion minor` after.
