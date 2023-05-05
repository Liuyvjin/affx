import os
import subprocess
import sys
from platform import system

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from pathlib import Path
PLATFORM = system()
BASE_DIR = Path(__file__).resolve().parent
BUILD_DIR = BASE_DIR / "build/"


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = str(BASE_DIR)


class CMakeBuild(build_ext):
    def run(self):
        # 检查 cmake 版本
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                'CMake must be installed to build the following extensions: ' +
                ', '.join(e.name for e in self.extensions)
            )

        # 开始构建 extensions
        BUILD_DIR.mkdir(exist_ok=True)
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        # cmake config
        build_type = 'Release'
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + str(BASE_DIR),  # 输出在根目录下
                      f'-DCMAKE_BUILD_TYPE={build_type}',
                      '-DPYTHON_EXECUTABLE={}'.format(sys.executable) ]  # 指定 python

        if PLATFORM == 'Windows':
            cmake_args += ['-DCMAKE_TOOLCHAIN_FILE:STRING=E:/dev/vcpkg/scripts/buildsystems/vcpkg.cmake',
                            f'-S{str(BASE_DIR)}',
                            f'-B{str(BUILD_DIR)}',
                            '-G', 'Visual Studio 17 2022',
                            '-T', 'host=x64',
                            '-A', 'x64']

        subprocess.check_call(['cmake', str(BASE_DIR)] + cmake_args, cwd=str(BUILD_DIR))

        # build
        build_args = ['--config', build_type]
        subprocess.check_call(['cmake', '--build', '.', '--target', ext.name] + build_args , cwd=str(BUILD_DIR))

        # generate .pyi
        subprocess.check_call(['python', str(BASE_DIR/'stubgen.py'), '-p', str(BASE_DIR/'Release/'),
                                '-n', ext.name])

setup(
    name='PyAffx',
    version="0.0.1",
    description='',
    author='liujin',
    author_email='',
    url='',
    license='LGPL',
    ext_modules=[CMakeExtension('pyaffx')],
    cmdclass=dict(build_ext=CMakeBuild),
    keywords=['robot', 'robotics', 'trajectory-generation', 'motion-control'],
    python_requires='>=3.6',
    zip_safe=False,
)
