__author__ = 'Ben Fleischhacker'
LICENSE = '/l/CC/By'

import divisi2
import os
import re

curfp = os.path.abspath(__file__)
curdir = os.path.dirname(curfp)
#assertion (relation)[1] (concept1)[2] (concept2)[3] ctx (score)[4] contributer edge-id source surface
assertpat = r"\/a\/\[\/r\/\w+\/,\/c\/(?:%s)\/\w+\/,\/c\/(?:%s)\/\w+\/\]\s+\/r\/(\w+)\s+\/c\/\w+\/(\w+)\s+\/c\/\w+\/(\w+)\s+\S+\s+(\-?\d*\.?\d*)\s+\S+\s+\S+\s+\S+\s+\[.+\]"

def extractAssert(line, assertions_dict, assertpatc):
    m = re.match(assertpatc, line)
    if m is not None:
        #replace concepts who's spaces use relations
        rel = m.group(1).split('/')[0]
        c1 = m.group(2).split('/')[0].replace('_',' ')
        c2 = m.group(3).split('/')[0].replace('_','  ')
        assertion = "%s,%s,%s"%(rel, c1, c2) #remove r/ and c/(country code)/  from assertion
        #accumulate or init score for an assertion
        score = float(m.group(4))
        assertions_dict[assertion] = score+assertions_dict[assertion] if assertion in assertions_dict else score

def extractAsserts(csv_file, languages):
    langs = '|'.join(languages)
    assertpatc = re.compile(assertpat%(langs,langs))
    assertions = {}
    for line in csv_file:
        if line:
            line = line.strip()
            extractAssert(line, assertions, assertpatc)
    return assertions

def formTriples(assertions_dict, score_cutoff=0.0):
    for assertion,score in assertions_dict.items():
        rel,c1,c2 = assertion.split(',')
        if score > score_cutoff:
            yield score, c1, ('right', rel, c2)
            yield score, c2, ('left', rel, c1)

def buildMatrix(csv_filename, pickle_name, languages=['en'], cutoff=2):
    csv_file = open(csv_filename, 'rb')
    asserts_dict = extractAsserts(csv_file, languages)
    csv_file.close()
    triples = formTriples(asserts_dict)
    matrix = divisi2.make_sparse(triples)
    matrix = matrix.squish(cutoff)
    divisi2.save(matrix, pickle_name)


