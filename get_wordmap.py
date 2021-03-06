import sys


def load_wordmap(encoding='utf8', count_lower=True):
    wordmap = dict()
    with sys.stdin as fin:
        for line in fin:
            att = line.decode(encoding).strip().split('\t')[1:]
            for word in ' '.join(att).split():
                if word not in wordmap:
                    wordmap[word] = 1
                else:
                    wordmap[word] += 1
                if count_lower:
                    lower_word = word.lower()
                    if lower_word not in wordmap:
                        wordmap[lower_word] = 1
                    else:
                        wordmap[lower_word] += 1
    return wordmap


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(usage="Get Word Map")
    parser.add_argument('-lower', dest='lower', action='store_true', help='Count Raw and Lower')
    args = parser.parse_args()

    word_map = load_wordmap(args.lower)
    word_map = sorted(word_map.iteritems(), key=lambda d: d[1], reverse=True)
    with sys.stdout as out:
        for index, word_count in enumerate(word_map):
            write_str = "%s\t%s\t%s\n" % (word_count[0], index, word_count[1])
            out.write(write_str.encode('utf8'))
