# -*- coding: utf-8 -*-

"""General utilities for :mod:`rpy2`."""

import collections
import logging
from functools import lru_cache, wraps
from typing import Iterable, Tuple

from rpy2.robjects.packages import importr, isinstalled
from rpy2.robjects.vectors import StrVector

from .dsl import Variable

__all__ = [
    "uses_r",
]

logger = logging.getLogger(__name__)

# Using a forked version of causaleffect for version stability.
CRAN_REQUIREMENTS = ["igraph"]

GithubPackage = collections.namedtuple("GithubPackage", ["name", "url"])

GITHUB_REPO_REQUIREMENTS = [
    GithubPackage(
        "causaleffect",
        "https://github.com/altdeep/causaleffect.git"
    ),
]


def prepare_renv(
        cran_requirements: Iterable[str],
        github_requirements: Iterable[str]
    ) -> None:
    """Ensure the given R packages are installed.

    :param cran_requirements: A list of R packages in CRAN to ensure are installed
    :param github_requirements: A list of R packages in Github to ensure are installed

    .. seealso:: https://rpy2.github.io/doc/v3.4.x/html/introduction.html#installing-packages
    """
    # import R's utility package
    utils = importr("utils")
    devtools = importr("devtools")

    # select a mirror for R packages
    utils.chooseCRANmirror(ind=1)  # select the first mirror in the list

    uninstalled_cran_requirements = [
        requirement for requirement in cran_requirements if not isinstalled(requirement)
    ]
    if uninstalled_cran_requirements:
        logger.warning("installing R packages: %s", uninstalled_cran_requirements)
        utils.install_packages(StrVector(uninstalled_cran_requirements))

    # install github package requirements
    for package in github_requirements:
        devtools.install_github(package.url)

    for package_str in cran_requirements:
        importr(package_str)

    for package in github_requirements:
        importr(package.name)


@lru_cache(maxsize=1)
def prepare_default_renv() -> bool:
    """Prepare the default R environment."""
    prepare_renv(CRAN_REQUIREMENTS, GITHUB_REPO_REQUIREMENTS)
    return True


def uses_r(f):
    """Decorate functions that use R."""

    @wraps(f)
    def _wrapped(*args, **kwargs):
        prepare_default_renv()
        return f(*args, **kwargs)

    return _wrapped


def _parse_vars(element) -> Tuple[Variable, ...]:
    _vars = element.rx("vars")
    return tuple(Variable(name) for name in sorted(_vars[0]))


def _extract(element, key):
    return element.rx(key)[0][0]
