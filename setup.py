from setuptools import find_packages, setup

setup(
    name='leo',
    version='1.1',
    description='dict.leo.org',
    long_description='Leo Dictionary',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='leo',
    author='Andreas Stefl',
    author_email='stefl.andreas@gmail.com',
    url='https://github.com/andiwand/pyleo',
    license='GPLv3',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4>=4.3.0',
        'requests>=1.2.3',
        'lxml>=4.1.1',
    ],
    extras_require={
    },
    entry_points="""
    [console_scripts]
    leo=leo.leo:main
    train=leo.train:main
    """
)
