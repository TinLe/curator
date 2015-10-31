#!/usr/bin/env python
import os
import sys
import time
import logging
from datetime import timedelta, datetime, date

import elasticsearch
import curator

try:
    from logging import NullHandler
except ImportError:
    from logging import Handler

    class NullHandler(Handler):
        def emit(self, record):
            pass

__version__ = '2.1.0-dev'

# Elasticsearch versions supported
version_max  = (2, 0, 0)
version_min = (1, 0, 0)
        
logger = logging.getLogger(__name__)

DEFAULT_ARGS = {
    'host': 'localhost',
    'url_prefix': '',
    'port': 9200,
    'auth': None,
    'ssl': False,
    'timeout': 30,
    'prefix': 'logstash-',
    'suffix': '',
    'curation_style': 'time',
    'time_unit': 'days',
    'max_num_segments': 2,
    'dry_run': False,
    'debug': False,
    'log_level': 'INFO',
    'logformat': 'Default',
    'all_indices': False,
    'show_indices': False,
    'snapshot_prefix': 'curator-',
    'wait_for_completion': True,
    'ignore_unavailable': False,
    'include_global_state': True,
    'partial': False,
}

DATEMAP = {
    'months': '%Y.%m',
    'weeks': '%Y.%W',
    'days': '%Y.%m.%d',
    'hours': '%Y.%m.%d.%H',
}

def check_version(client):
    """
    Verify version is within acceptable range.  Exit with error if it is not.
    
    :arg client: The Elasticsearch client connection
    """
    version_number = curator.get_version(client)
    logger.debug('Detected Elasticsearch version {0}'.format(".".join(map(str,version_number))))
    if version_number >= version_max or version_number < version_min:
        print('Expected Elasticsearch version range > {0} < {1}'.format(".".join(map(str,version_min)),".".join(map(str,version_max))))
        print('ERROR: Incompatible with version {0} of Elasticsearch.  Exiting.'.format(".".join(map(str,version_number))))
        sys.exit(1)


def main():
    client = elasticsearch.Elasticsearch()
    check_version(client)
    for index_name in curator.get_indices(client):
        print("index: {0}".format(index_name))


if __name__ == '__main__':
    main()
