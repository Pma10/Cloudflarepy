from setuptools import setup, find_packages

from cloudflarepy import __version__

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='cloudflarepy',
    version=__version__,
    description='Cloudflare API Python Wrapper',
    author='Pma10',
    author_email='pmavmak10@gmail.com',
    url='https://github.com/Pma10/Cloudflarepy',
    install_requires=requirements,
    packages=find_packages(exclude=[]),
    keywords=["api", "cloudflare", "pma"],
    python_requires='>=3.9',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)