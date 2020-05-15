from distutils.core import setup

setup(
    name='fundamentos',
    packages=['fundamentos'],
    version='1.0',
    license='MIT',
    description='Download Bovespa Stock Market fundamentals with Python.',
    author='Nathan de Moura Vieira',
    author_email='nathanmoura194@gmail.com',
    url='https://github.com/NathanMoura/fundamentos',
    download_url='https://github.com/NathanMoura/fundamentos/archive/v1.0.tar.gz',
    keywords=['pandas', 'finance', 'fundamentals', 'bovespa'],
    install_requires=[
        'pandas',
        'requests',
        'lxml'
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
