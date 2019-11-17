from setuptools import setup, find_packages

from seaweedfs import __VERSION__

with open("requirements.txt", "r") as fp:
    requirements = fp.readlines()

setup(
    name="seaweedfs-py",
    version=__VERSION__,
    description="client of seaweedfs",
    author="george wang",
    author_email="georgewang1994@163.com",
    url="https://github.com/GeorgeWang1994/seaweedfs-py",
    install_requires=requirements,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
)
