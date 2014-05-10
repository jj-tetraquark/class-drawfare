import unittest
import re
from pprint import pformat
import cpp_parsing


class TestCPPParser(unittest.TestCase):

    def test_strip_comments(self):
        string_with_comments = """No comments in this string
            // This is a single line comment, it should be gone
            // This should also disappear
            None at all
            /*
                This is a multiline comment, it should also go
            */
            """
        result = """No comments in this string
            None at all"""

        stripped = cpp_parsing.strip_comments(string_with_comments)
        # don't care about whitespace
        stripped = re.sub('\s+', ' ', stripped).strip()
        result = re.sub('\s+', ' ', result).strip()
        self.assertEqual(stripped, result)

    def test_get_methods(self):
        code = """
            int testMethod1();
            void Test2Method(const Ref& erence,
                int anotherThing, namespaced::thing x);

            const unsigned int method();
            static const bool StaticMethod(thing);
            lots::of::namespaces<oohAType> method();
            bool canYouHandleAnInlineMethod() { return true; }

            friend long double theseKeywordsWork();

            dontMatchThis(true);
            """

        methods_and_positions = cpp_parsing.get_methods(code)
        methods = [x[1] for x in methods_and_positions]

        self.assertEqual("int testMethod1()",  methods[0])
        self.assertEqual(
            "void Test2Method(const Ref& erence, int anotherThing, "
            "namespaced::thing x)", methods[1])

        self.assertEqual("const unsigned int method()", methods[2])
        self.assertEqual("static const bool StaticMethod(thing)", methods[3])
        self.assertEqual("lots::of::namespaces<oohAType> method()", methods[4])
        self.assertEqual("bool canYouHandleAnInlineMethod()", methods[5])
        self.assertEqual("friend long double theseKeywordsWork()", methods[6])

        self.assertEqual(len(methods), 7,
                         "expected 7 methods but got {0} \n {1}"
                         .format(len(methods), pformat(methods)))


if __name__ == "__main__":
    unittest.main()
