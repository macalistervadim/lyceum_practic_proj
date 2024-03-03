import unittest


def suite():
    loader = unittest.TestLoader()
    start_dir = "catalog"
    return loader.discover(start_dir)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())


__all__ = []
