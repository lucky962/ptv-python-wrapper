from setuptools import setup, find_packages

setup(
    name='ptv-python-wrapper',
    version='0.1.1',
    packages=find_packages(),
    description='An API Wrapper for Public Transport Victoria (PTV)',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/lucky962/ptv-python-wrapper',
    license='MIT',
    author='Leo Terray',
    author_email='leoterray@yahoo.com.au',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['ptv', 'melbourne', 'victoria', 'public transport'],
    install_requires=['requests'],
    tests_require=['pytest'],
)