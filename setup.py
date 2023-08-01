from setuptools import setup


def main():
    """
    Setup the package

    """
    setup(
        setup_requires=["setuptools_scm"],
        use_scm_version={"write_to": "profet/_version.py"},
    )


if __name__ == "__main__":
    main()
