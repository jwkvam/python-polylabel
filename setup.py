"""Packaging code."""
from setuptools import setup, find_packages


# https://packaging.python.org/guides/single-sourcing-package-version/
def read(*parts):
    """Read contents of a file."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    """Find version in a file."""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="python-polylabel",
    version=find_version('polylabel', '__init__.py'),
    author='Michal Hatak',
    author_email='me@twista.cz',
    packages=find_packages(),
    description='Port of polylabel (made by MapBox - https://github.com/mapbox/polylabel)',
    long_description=__doc__,
)
