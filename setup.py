import os
from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(BASEDIR)  # For relative `packages` spec in setup below


def get_version():
    """ Find the version of the package"""
    version = None
    version_file = os.path.join(BASEDIR, 'ovos_workshop', 'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


def get_description():
    with open(os.path.join(BASEDIR, "README.md"), "r") as f:
        long_description = f.read()
    return long_description


# PAS de nom pip renommé, contrairement aux autres forks 202home (wifi-
# setup, pulseaudio) — RÉGRESSION CONSTATÉE EN VRAI : ovos-core==2.1.1
# déclare `Requires-Dist: ovos-workshop<8.0.0,>=7.0.6` (vérifié dans ses
# métadonnées PyPI). Renommer notre distribution en 202home-ovos-workshop
# faisait perdre à pip toute trace d'un paquet satisfaisant CE nom-là : au
# `pip install ovos-core==2.1.1` suivant, pip réinstallait silencieusement
# le VRAI ovos-workshop de PyPI par-dessus notre fork (même dossier de
# module ovos_workshop, donc écrasement direct) — @tag_handler
# disparaissait, le skill ne se chargeait plus
# (« cannot import name 'tag_handler' »), constaté en vrai sur un build
# réel. Le nom de distribution DOIT rester identique à l'amont pour que
# pip continue de reconnaître notre fork comme la réponse à cette
# dépendance — l'ambiguïté pip list/pip show est un moindre mal ici.
setup(
    name='ovos_workshop',
    version=get_version(),
    packages=['ovos_workshop',
              'ovos_workshop.skills',
              'ovos_workshop.decorators'],
    install_requires=required("requirements/requirements.txt"),
    extras_require={
        'ocp': required('requirements/ocp.txt')
    },
    package_data={'': package_files('ovos_workshop')},
    url='https://github.com/OpenVoiceOS/OVOS-workshop',
    license='apache-2.0',
    author='jarbasAi',
    author_email='jarbasai@mailfence.com',
    include_package_data=True,
    description='frameworks, templates and patches for the OpenVoiceOS universe',
    long_description=get_description(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'ovos-skill-launcher=ovos_workshop.skill_launcher:_launch_script'
        ]
    }
)
