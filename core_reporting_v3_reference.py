#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Reference command-line example for Google Analytics Core Reporting API v3.

This application demonstrates how to use the python client library to access
all the pieces of data returned by the Google Analytics Core Reporting API v3.

The application manages autorization by saving an OAuth2.0 token in a local
file and reusing the token for subsequent requests.

Before You Begin:

Update the client_secrets.json file

  You must update the clients_secrets.json file with a client id, client
  secret, and the redirect uri. You get these values by creating a new project
  in the Google APIs console and registering for OAuth2.0 for installed
  applications: https://code.google.com/apis/console

  Learn more about registering your analytics application here:
  http://developers.google.com/analytics/devguides/reporting/core/v3/gdataAuthorization

Supply your TABLE_ID

  You will also need to identify from which profile to access data by
  specifying the TABLE_ID constant below. This value is of the form: ga:xxxx
  where xxxx is the profile ID. You can get the profile ID by either querying
  the Management API or by looking it up in the account settings of the
  Google Anlaytics web interface.

Sample Usage:

  $ python core_reporting_v3_reference.py ga:xxxx

Where the table ID is used to identify from which Google Anlaytics profile
to retrieve data. This ID is in the format ga:xxxx where xxxx is the
profile ID.

Also you can also get help on all the command-line flags the program
understands by running:

  $ python core_reporting_v3_reference.py --help
"""
from __future__ import print_function

__author__ = 'api.nickm@gmail.com (Nick Mihailovski)'
# modified by Kelly Rowland for Berkeley Research Computing

import argparse
import sys
import datetime

from googleapiclient.errors import HttpError
from googleapiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('table_id', type=str,
                     help=('The table ID of the profile you wish to access. '
                           'Format is ga:xxx where xxx is your profile ID.'))


def main(argv):

  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'analytics', 'v3', __doc__, __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/analytics.readonly')

  # dates between which to collect data
  # note that the HPC sites were first launched on September 18, 2014
  start = datetime.date(2015,1,1)
  end = datetime.date(2015,12,31)
  num_days = end - start
  date_list = [end - datetime.timedelta(days=x) for x in range(0, num_days.days+1)]
  date_strings = []
  for date in date_list:
    month = "%02d" % (date.month,) # append leading zero if needed
    day = "%02d" % (date.day,)     # append leading zero if needed
    date_strings.insert(0,(str(date.year)+'-'+str(month)+'-'+str(day))) 

  # Try to make a request to the API. Print the results or handle errors.
  try:
    outfile = open("2015.txt","w")
    for date in date_strings:
      results = get_api_query(service, flags.table_id,date,date).execute()
      print_results(results,date,outfile)
    outfile.close()

  except TypeError as error:
    # Handle errors in constructing a query.
    print(('There was an error in constructing your query : %s' % error))

  except HttpError as error:
    # Handle API errors.
    print(('Arg, there was an API error : %s : %s' %
           (error.resp.status, error._get_reason())))

  except AccessTokenRefreshError:
    # Handle Auth errors.
    print ('The credentials have been revoked or expired, please re-run '
           'the application to re-authorize')


def get_api_query(service, table_id,start,end):
  """Returns a query object to retrieve data from the Core Reporting API.

  Args:
    service: The service object built by the Google API Python client library.
    table_id: str The table ID form which to retrieve data.
  """

  return service.data().ga().get(
      ids=table_id,
      # this is the first date that Google Analytics has a non-zero number of views for
#      start_date='2014-09-18',
#      end_date='2014-09-18',
      start_date = start,
      end_date = end,
      metrics='ga:pageviews',
      dimensions='ga:pagePathLevel2,ga:pagePathLevel3',
#      sort='-ga:pageviews',
      start_index='1',
      max_results='5000')


def print_results(results,date,outfile):
  """Prints all the results in the Core Reporting API Response.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print_rows(results,date,outfile)


def print_rows(results,date,outfile):
  """Prints all the rows of data returned by the API.

  Args:
    results: The response returned from the Core Reporting API.
  """

#  print('Rows:')
  if results.get('rows', []):
    for row in results.get('rows'):
      # only looking for HPC pages right now
      if u'/high-performance-computing/' in row:
        # every page has the HPC bit as the first row entry, so remove it
        del row[0]
        outfile.write('\t'.join(row)+'\t'+str(date)+'\n')
  else:
    print('No Rows Found')


if __name__ == '__main__':
  main(sys.argv)
