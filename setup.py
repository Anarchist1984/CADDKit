from setuptools import setup, find_packages

setup(
    name='caddkit',
    version='0.1.0-dev',
    author='George Mathew',
    author_email='nerd2923@gmail.com',
    description='A brief description of your package',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Anarchist1984/CADDKit',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=open('requirements.txt', encoding="utf-8").read().splitlines(),
    extras_require={
        'dev': open('dev-requirements.txt', encoding="utf-8").read().splitlines(),
    },
)