from setuptools import setup, find_packages

setup(
    name="MNaseSeqTools",
    version="0.1-SNAPSHOT",
    packages=find_packages(),
    author="Christian Poitras",
    author_email="christian.poitras@ircm.qc.ca",
    description="Tools to analyze MNase-seq data",
    keywords="bioinformatics, MNase-seq",
    url="https://github.com/francoisrobertlab/mnase-201908",
    license='GNU General Public License version 3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License version 3'
    ],
    python_requires='>=3.7.4',
    install_requires=[
        'click>=7.0',
        'pandas>=0.25.0',
        'seqtools@http://github.com/francoisrobertlab/seqtools/tarball/0.1.1'
    ],
    entry_points={
        'console_scripts': [
            'prepgenecov = checseqtools.PrepareGenomeCoverage:main',
            'fullanalysis = checseqtools.FullAnalysis:main'
        ]
    }
)