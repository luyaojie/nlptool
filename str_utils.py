#!/usr/bin/env python
# -*- coding:utf-8 -*- 


class StrStartLengthMatcher:
    """
    Check different overlap match
    """

    @staticmethod
    def exact_match(s1, l1, s2, l2):
        """
        :param s1: Str1 Start
        :param l1: Str1 Length
        :param s2: Str2 Start
        :param l2: Str2 Length
        :return:
        """
        return s1 == s2 and s1 + l1 == s2 + l2

    @staticmethod
    def partial_match(s1, l1, s2, l2):
        """
        :param s1: Str1 Start
        :param l1: Str1 Length
        :param s2: Str2 Start
        :param l2: Str2 Length
        :return:
        """
        e1 = s1 + l1 - 1
        e2 = s2 + l2 - 1
        if s1 > e2 or s2 > e1:
            return False
        else:
            return True

    @staticmethod
    def include_match(s1, l1, s2, l2):
        """
        :param s1: Str1 Start
        :param l1: Str1 Length
        :param s2: Str2 Start
        :param l2: Str2 Length
        :return:
        """
        if s1 <= s2 and s1 + l1 >= s2 + l2:
            return True
        elif s2 <= s1 and s2 + l2 >= s1 + l1:
            return True
        else:
            return False


def find_substr_in_str(text, target, end_close_interval=False):
    """
    Find substr in string
    :param text:
    :param target:
    :param end_close_interval:
    :return:
        [(start1, end1), (start2, end2), ]
        if end_close_interval is True:
            ends are the indexes of last char in matched string
        else:
            ends are the indexes of first char after matched string
    """
    import re
    if end_close_interval:
        ret = [(m.start(), m.end() - 1) for m in re.finditer(re.escape(target), text)]
    else:
        ret = [(m.start(), m.end()) for m in re.finditer(re.escape(target), text)]
    return ret


def main():
    text = "abcabcabc"
    target = "b"
    print(find_substr_in_str(text, target, end_close_interval=True))
    print(find_substr_in_str(text, target, end_close_interval=False))


if __name__ == "__main__":
    main()
