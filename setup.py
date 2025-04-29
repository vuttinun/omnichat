# omnichat/setup.py
from setuptools import setup, find_packages

setup(
    name="omnichat",
    version="1.0.1",
    description="OmniChat integration with multiple LINE Messaging API accounts for ERPNext",
    author="Vuttinun",
    author_email="vuttinunboontang@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "frappe",
        "requests"
    ],
    license="MIT"
)
