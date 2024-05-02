from setuptools import setup

setup(
    name='treqs',
    version='1.0.0',
    py_modules=['treqs'],
    install_requires=[
        'Click',
        'pyyaml',
        'lxml'
    ],
    packages=['treqs'],
    entry_points='''
        [console_scripts]
        treqs=treqs.main:treqs
    ''',
    extras_require={
        'dev': [
            'coverage',
            'coverage-badge'
        ]
    }
)
