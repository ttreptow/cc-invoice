from setuptools import setup


setup(
    name="cc-invoice",
    version="0.0.1",
    description="Example application using Python and Flask",
    author="Tim Treptow",
    author_email="tim.treptow@gmail.com",
    url="https://github.com/ttreptow/cc-invoice",
    install_requires=["flask", "flask-sqlalchemy", "werkzeug"]
)
