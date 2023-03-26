from setuptools import setup

setup(
    name='MyFastApiApp',
    version='0.0.1',
    author='mrgo1d',
    author_email='alejandroustin@gmail.com',
    description='FastApi application',
    install_requires=[
        "fastapi==0.95.0",
        "pytest==7.2.2",
        "SQLAlchemy==2.0.7",
        "uvicorn==0.21.1"
    ],
    scripts=['app/main.py'],
    python_requires='==3.11'
)
