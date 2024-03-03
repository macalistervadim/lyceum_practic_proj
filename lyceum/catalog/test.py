import unittest


def suite():
    loader = unittest.TestLoader()
    start_dir = "tests"
    suite = loader.discover(start_dir)
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())


__all__ = []
