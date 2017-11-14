from setuptools import setup

setup(
    name='calendar_fetcher_pckg',
    version='0.1',
    description='Fetch information from your calendar',
    url='https://github.com/tomasruizt/calendar_fetcher_pckg',
    author='Tomas Ruiz',
    author_email='tomas.ruiz.te@gmail.com',
    packages=[
        'calendar_fetcher_pckg',
    ],
    zip_safe=False,
    install_requires=[
        'google-api-python-client',
        'httplib2'
    ],
)
