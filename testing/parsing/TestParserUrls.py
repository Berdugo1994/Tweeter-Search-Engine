import unittest
from timeit import default_timer as timer
from parser_module import Parse


class TestParserUrls(unittest.TestCase):
    def test_url1(self):
        # Test 4
        text = "edennnn https://www.instagram.com/p/CD7fAPWs3WM/?igshid=o9kf0ugp1l8x eden king http://Berdugo94.github.io/test check"
        expected = ["https", "www", "instagram.com", "p", "CD7fAPWs3WM", "igshid", "o9kf0ugp1l8x", "http",
                    "Berdugo94.github.io", "test",
                    "edennnn", "eden", "king", "check"]
        start = timer()
        actual = Parse().parse_sentence(text)
        end = timer()
        # print('\n' + "Time of test 4 is :" + (str(end - start)))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
