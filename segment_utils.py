# -*- coding: utf-8 -*-
import codecs


def any2utf8(text, errors='strict', encoding='utf8'):
    """Convert a string (unicode or bytestring in `encoding`), to bytestring in utf8."""
    if isinstance(text, unicode):
        return text.encode('utf8')
    # do bytestring -> unicode -> utf8 full circle, to ensure valid utf8
    return unicode(text, encoding, errors=errors).encode('utf8')


def write_str_to_out(out, write_str):
    out.write(any2utf8(write_str))


class ChineseWordSegmentor(object):
    def __init__(self, model='jieba'):
        self.model = model
        if model.lower() == 'jieba':
            import jieba.posseg as posseg
            posseg.initialize()
            self.segmentor = posseg.POSTokenizer(tokenizer=None)
        elif model.lower() == 'ictclas':
            import pynlpir
            pynlpir.open()
            self.segmentor = pynlpir
        else:
            raise NotImplementedError

    def segment(self, text, pos=False):
        """
        The segmented tokens are returned as a list. Each item of the list is a
        string if *pos* is `False`, e.g. ``['我们', '是', ...]``. If
        *pos* is `True`, then each item is a tuple (``(token, pos)``), e.g.
        ``[('我们', 'pronoun'), ('是', 'verb'), ...]``.
        :param text:
        :param pos:
        :return:
        """
        if self.model.lower() == 'jieba':
            if pos:
                return [token for token in self.segmentor.cut(text)]
            else:
                return [tuple(token)[0] for token in self.segmentor.cut(text)]
        elif self.model.lower() == 'ictclas':
            if pos:
                return self.segmentor.segment(text, pos_tagging=True)
            else:
                return self.segmentor.segment(text, pos_tagging=False)
        else:
            raise NotImplementedError


if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Chinese Word Segmentation')
    parser.add_argument('-s', '--src', default="stdin", type=str, dest="src",
                        help='raw file, default is stdin')
    parser.add_argument('-t', '--tar', default="stdout", type=str, dest="tar",
                        help='segmented file, default is stdout')
    parser.add_argument('-seg', default="ictclas", type=str, dest="seg",
                        help='segment type, default is ictclas, (ictclas jieba)')
    parser.add_argument('-pos', action="store_true", dest="pos",
                        help='keep pos, default is False')
    args = parser.parse_args()
    segger = ChineseWordSegmentor(args.seg)
    with sys.stdin if args.src == 'stdin' else codecs.open(args.src, 'r', 'utf8') as fin:
        with sys.stdout if args.tar == 'stdout' else codecs.open(args.tar, 'w') as out:
            for line in fin:
                if args.src == 'stdin':
                    line = line.decode('utf8')
                line = line.strip()
                if len(line) == 0:
                    out.write('\n')
                try:
                    result = segger.segment(line, pos=args.pos)
                    if args.pos:
                        seg_result = u" ".join(["/".join(r) for r in result])
                    else:
                        seg_result = u" ".join(result)
                    to_write = seg_result + '\n'
                except:
                    to_write = u' '.join(list(line)) + '\n'
                    sys.stderr.write(any2utf8(to_write))
                write_str_to_out(out, to_write)
