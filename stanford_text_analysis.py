#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Created by Roger on 2018/1/12
import json
import requests
from multiprocessing import Pool
import sys

default_properties = {
    'annotators': 'tokenize,ssplit,pos,ner,depparse',
    'outputFormat': 'json'
}


class StanfordCoreNLP:
    # Almost from https://github.com/smilli/py-corenlp/blob/master/pycorenlp/corenlp.py
    # Some Change text in annotate must encoded in some coding, such as utf8
    def __init__(self, server_url):
        if server_url[-1] == '/':
            server_url = server_url[:-1]
        self.server_url = server_url

    def annotate(self, text, properties=None, encoding=None):
        if properties is None:
            properties = {}
        else:
            assert isinstance(properties, dict)

        # Checks that the Stanford CoreNLP server is started.
        try:
            requests.get(self.server_url)
        except requests.exceptions.ConnectionError:
            raise Exception('Check whether you have started the CoreNLP server e.g.\n'
                            '$ cd stanford-corenlp-full-2015-12-09/ \n'
                            '$ java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer')

        if encoding is None:
            data = text
        else:
            data = text.encode('utf8')

        r = requests.post(
            self.server_url, params={
                'properties': str(properties)
            }, data=data, headers={'Connection': 'close'})
        output = r.text
        if ('outputFormat' in properties
                and properties['outputFormat'] == 'json'):
            try:
                output = json.loads(output, encoding='utf-8', strict=True)
            except:
                sys.stderr.write("Skip Error Run: %s" % data)
        return output


def load_parsed_json(json_filename):
    parsed_json = dict()
    with open(json_filename, 'r') as fin:
        for line in fin:
            line, p_json = line.strip().split("\t")
            parsed_json[line] = p_json
    return parsed_json


def main():
    import codecs
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Stanford Text Analyzer")
    parser.add_argument('-server', dest='server', type=str, default="127.0.0.1", help='Stanford Corenlp Server URL')
    parser.add_argument('-port', dest='port', type=int, default=8080, help='Stanford Corenlp Server Port')
    parser.add_argument('-input', dest='input', type=str, default=None, required=True,
                        help='Input File Name, one text one line')
    parser.add_argument('-output', dest='output', type=str, default=None, required=True,
                        help='Output File Name, each line: text\tparsed json')
    parser.add_argument('-encoding', dest='encoding', type=str, default='utf8',
                        help='Input File Encoding')
    parser.add_argument('-annotators', dest='annotators', type=str, default='tokenize,ssplit,pos,ner,depparse',
                        help='Stanford Corenlp Annotators')
    args = parser.parse_args()

    properties = {
        'annotators': args.annotators,
        'outputFormat': 'json'
    }

    nlp = StanfordCoreNLP('http://%s:%s' % (args.server, args.port))

    with open(args.output, 'w') as output:
        with codecs.open(args.input, 'r', args.encoding) as fin:
            for line in fin:
                line = line.strip().replace('\t', ' ')
                parsed_json = nlp.annotate(text=line, encoding=args.encoding, properties=properties)
                output.write("%s\t%s\n" % (line, json.dumps(parsed_json)))


if __name__ == "__main__":
    main()
