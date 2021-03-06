# -*- coding: utf-8 -*-

import os
import warnings

import pytest

import camelot


testdir = os.path.dirname(os.path.abspath(__file__))
testdir = os.path.join(testdir, "files")
filename = os.path.join(testdir, 'foo.pdf')


def test_unknown_flavor():
    message = ("Unknown flavor specified."
               " Use either 'lattice' or 'stream'")
    with pytest.raises(NotImplementedError, message=message):
        tables = camelot.read_pdf(filename, flavor='chocolate')


def test_input_kwargs():
    message = "columns cannot be used with flavor='lattice'"
    with pytest.raises(ValueError, message=message):
        tables = camelot.read_pdf(filename, columns=['10,20,30,40'])


def test_unsupported_format():
    message = 'File format not supported'
    filename = os.path.join(testdir, 'foo.csv')
    with pytest.raises(NotImplementedError, message=message):
        tables = camelot.read_pdf(filename)


def test_stream_equal_length():
    message = ("Length of table_area and columns"
               " should be equal")
    with pytest.raises(ValueError, message=message):
        tables = camelot.read_pdf(filename, flavor='stream',
            table_area=['10,20,30,40'], columns=['10,20,30,40', '10,20,30,40'])


def test_no_tables_found():
    filename = os.path.join(testdir, 'blank.pdf')
    # TODO: use pytest.warns
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        try:
            tables = camelot.read_pdf(filename)
        except Exception as e:
            assert type(e).__name__ == 'UserWarning'
            assert str(e) == 'No tables found on page-1'