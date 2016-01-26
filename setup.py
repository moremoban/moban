try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='moban',
    author="C. W.",
    version="0.0.1",
    author_email="wangc_2011 (at) hotmail.com",
    description='Apply jinja2 on static file generation',
    install_requires=['pyyaml==3.11', 'jinja2==2.7.1'],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    long_description="test",
    zip_safe=False,
    tests_require=['nose'],
    license='New BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
    ],
    entry_points={
        'console_scripts':[
            'moban = moban.template:main'
        ]
    }
)
