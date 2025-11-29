from setuptools import setup

setup(
    name="ukg-api-client",
    version="1.0.0",
    description="UKG API Client for workforce management",
    py_modules=["ukg_api_client"],
    install_requires=["requests"],
    python_requires=">=3.7",
)