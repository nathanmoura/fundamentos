from setuptools import setup

# twine check dist/* pra ver se n tem nada de errado
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='fundamentos',
    packages=['fundamentos'],
    version='1.5',  # Atualizar
    license='MIT',
    description='Download Bovespa Stock Market fundamentals with Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nathan de Moura Vieira',
    author_email='nathanmoura194@gmail.com',
    url='https://github.com/NathanMoura/fundamentos',
    download_url='https://github.com/NathanMoura/fundamentos/archive/v1.5.tar.gz',  # Atualizar
    keywords=['pandas', 'finance', 'fundamentals', 'bovespa'],
    install_requires=[
        'pandas',
        'requests',
        'lxml',
        'xlrd'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',

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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

    ],
)
