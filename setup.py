from setuptools import setup

# twine check dist/* pra ver se n tem nada de errado
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='fundamentos',
    packages=['fundamentos'],
    version='1.2',
    license='MIT',
    description='Download Bovespa Stock Market fundamentals with Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nathan de Moura Vieira',
    author_email='nathanmoura194@gmail.com',
    url='https://github.com/NathanMoura/fundamentos',
    download_url='https://github.com/NathanMoura/fundamentos/archive/v1.2.tar.gz',
    keywords=['pandas', 'finance', 'fundamentals', 'bovespa'],
    install_requires=[
        'pandas',
        'requests',
        'lxml',
        'xlrd'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',

        'Operating System :: OS Independent',

        'Intended Audience :: Developers',

        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

    ],
)
