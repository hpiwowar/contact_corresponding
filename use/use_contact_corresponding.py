#!/usr/bin/env python
# encoding: utf-8
"""
@author: Heather Piwowar
@contact:  hpiwowar@gmail.com
"""

import sys
import os
import nose
from nose.tools import assert_equals
import csv

import contact_corresponding

if __name__ == '__main__':
    nose.runmodule()

def get_this_dir(): 
    module = sys.modules[__name__]
    this_dir = os.path.dirname(os.path.abspath(module.__file__))
    return(this_dir)

data_path = os.path.join(get_this_dir(), "data")
isi_output_filename = os.path.join(get_this_dir(), "output.csv")
scopus_output_filename = os.path.join(get_this_dir(), "scopus_output.csv")

class TestStuff(object):
    def test_get_all_isi_journal_month_year_email(self):
        print(data_path)
        response = contact_corresponding.get_isi_all_journal_year_month_email(data_path)
        assert_equals(response[0:5], [('FEBS Lett.', '2010', 'DEC', ['Israel.Pecht@weizmann.ac.il']), ('FEBS Lett.', '2010', 'DEC', ['rgermain@nih.gov']), ('FEBS Lett.', '2010', 'DEC', ['Michael.Dustin@med.nyu.edu']), ('FEBS Lett.', '2010', 'DEC', ['molnar@immunbio.mpg.de', 'deswal@immunbio.mpg.de', 'schamel@immunbio.mpg.de']), ('FEBS Lett.', '2010', 'DEC', ['jane.oliaro@petermac.org'])])
        
        journals = [journal for (journal, year, month, email) in response]
        assert_equals(len(set(journals)), 47)

        years = [year for (journal, year, month, email) in response]
        assert_equals(year, "2010")
        
        months = [month for (journal, year, month, email) in response]
        assert_equals(set(months), set(['', 'MAR', 'FEB', 'AUG', 'SEP', 'MAY', 'WIN', 'SUM', 'JUN', 'JUL', 'JAN', 'APR', 'SPR', 'FAL', 'NOV', 'DEC', 'OCT']))

        #writer = csv.writer(open(isi_output_filename, "w"))
        #writer.writerows(response)

    def test_get_all_scopus_journal_month_year_email(self):
        print(data_path)
        response = contact_corresponding.get_scopus_all_journal_year_month_email(data_path)
        assert_equals(response[0:5], [('American Naturalist', '2010', '', ['dkikuchi@email.unc.edu']), ('American Naturalist', '2010', '', ['nigel.raine@rhul.ac.uk']), ('American Naturalist', '2010', '', ['marjo.saastamoinen@helsinki.fi']), ('American Naturalist', '2010', '', ['sonya.auer@email.ucr.edu']), ('American Naturalist', '2010', '', ['jbyoder@gmail.com'])])
        
        journals = [journal for (journal, year, month, email) in response]
        assert_equals(len(set(journals)), 52)

        years = [year for (journal, year, month, email) in response]
        assert_equals(year, "2010")
        
        #months = [month for (journal, year, month, email) in response]
        #assert_equals(set(months), set(['', 'MAR', 'FEB', 'AUG', 'SEP', 'MAY', 'WIN', 'SUM', 'JUN', 'JUL', 'JAN', 'APR', 'SPR', 'FAL', 'NOV', 'DEC', 'OCT']))

        writer = csv.writer(open(scopus_output_filename, "w"))
        writer.writerows(response)        