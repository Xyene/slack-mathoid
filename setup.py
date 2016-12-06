from setuptools import setup

setup(
    name='slack-mathoid',
    version='0.1',
    packages=['slack-mathoid'],
    entry_points={
        'console_scripts': [
            'slack-mathoid = slack-mathoid.server:main',
        ]
    },
    install_requires=['tornado'],

    author='Tudor Brindus',
    author_email='me@tbrindus.ca',
    url='https://github.com/DMOJ/slack-mathoid',
    description='LaTeX math integration for Slack.',
    classifiers=[
        'Development Status :: 3 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Software Development',
    ],
)
