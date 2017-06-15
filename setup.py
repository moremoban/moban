from setuptools import setup, find_packages


NAME = 'moban'
AUTHOR = 'C.W.'
VERSION = '0.0.6'
EMAIL = "wangc_2011 (at) hotmail.com"
LICENSE = 'MIT'
ENTRY_POINTS = {
    'console_scripts': [
        '%s = moban.main:main' % NAME
    ]
}
PACKAGES = find_packages(exclude=['ez_setup', 'examples', 'tests'])
DESCRIPTION = 'Yet another jinja2 cli command for static text generation'
INSTALL_REQUIRES = ['pyyaml>=3.11', 'jinja2>=2.7.1']
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Developers',
]


def read_files(*files):
    text = ""
    for single_file in files:
        text = text + read(single_file) + "\n"
    return text


def read(afile):
    with open(afile, 'r') as opened_file:
        return opened_file.read()


if __name__ == '__main__':
    setup(
        name=NAME,
        author=AUTHOR,
        version=VERSION,
        author_email=EMAIL,
        description=DESCRIPTION,
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        include_package_data=True,
        long_description=read_files('README.rst', 'CHANGELOG.rst'),
        zip_safe=False,
        tests_require=['nose'],
        license=LICENSE,
        classifiers=CLASSIFIERS,
        entry_points=ENTRY_POINTS
    )
