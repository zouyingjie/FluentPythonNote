# -*- coding: utf-8 -*-

from collections import namedtuple
from enum import Enum

Result = namedtuple("Result", "status data")

HTTPStatus = Enum('Status', 'ok not_found_error')

POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

SERVERS = {
    'REMOTE': 'http://flupy.org/data/flags',
    'LOCAL': 'http://localhost:8001/flags',
    'DELAY': 'http://localhost:8002/flags',
    'ERROR': 'http://localhost:8003/flags',
}

DEFAULT_SERVER = 'LOCAL'

DEST_DIR = './'

COUNTRY_CODES_FILE = 'country_codes.txt'
