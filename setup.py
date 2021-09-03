import setuptools
import pathlib

INSTALL_REQUIRES = [
    "django >= 3.2.6",
    "gitcalendar >= 1.0.0"
]

DEVELOP_REQUIRES = [
    "reuse>=0.12.1",
    "wheel",
    "twine",
]

EXTRAS_REQUIRE = {
    "develop": DEVELOP_REQUIRES,
}

package = setuptools.find_packages()

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="gitcalendar-webservice",
    version="0.8",
    author="Benjamin Moritz Bauer",
    author_email="benjamin.bauer@dlr.de",
    maintainer="Deutsches Zentrum fuer Luft- und Raumfahrt e.V. (DLR)",
    description="Webservice that implements the python library GitCalendar, "
                "which generates an ICS file from issues, milestones and iterations,"
                " of one or more GitLab projects.",
    long_description=README,
    long_description_content_type='text/markdown',
    url="https://gitlab.com/dlr-sc/gitcalendar-webservice",
    license='License :: MIT',
    packages=package,
    # entry_points={
    #    'console_scripts': [
    #        'gitcalendar=gitcalendar.gitcalendar:cli',
    #    ],
    # },
    classifiers=[
        "Environment :: Web Environment"
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 3.2",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=[
        'ics',
        'ical',
        'calendar',
        'icalendar',
        'gitlab',
        'django',
    ],
    python_requires=">=3.9",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
)
