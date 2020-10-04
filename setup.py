import setuptools

import OpenWeChat

with open('README.rst') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = [line.strip() for line in f]

setuptools.setup(
    name='OpenWechat',
    version=OpenWeChat.__version__,
    author='Abraham',
    author_email='abraham.liu@hotmail.com',
    description='A Open WeChat development kit',
    long_description=long_description,
    long_description_content_type='text/rst',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)
