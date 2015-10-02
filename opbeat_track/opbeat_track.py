import argparse
import json
import logging
import urllib2
import subprocess

"""
###############################################################

DEFAULT APP CREDENTIALS

Change these if you want to hard code the values and avoid
using the optional arguments every time you track a release.
"""

default_credentials = {
    'app_id': 'xxxxx',
    'org_id': 'xxxxx',
    'secret_token': 'xxxxx',
}

"""
###############################################################
"""

package_name = 'opbeat-track'
__version__ = "0.0.1"


def get_data_from_git(command):
    """
    Runs a command as a subprocess and returns the output
    """
    PIPE = subprocess.PIPE

    process = subprocess.Popen(
        command.split(),
        stdout=PIPE,
        stderr=PIPE
    )

    stdoutput, stderroutput = process.communicate()

    if stderroutput:
        # Handle errors
        logging.error('Something went wrong:')
        logging.error(stderroutput)
        exit(1)
    else:
        # Success!
        return stdoutput.strip()


def parse_credentials(arguments):
    """
    Parses credentials in the form of arguments or from the default set above
    and checks for missing or empty keys
    """
    credentials = {}

    credential_keys = ['app_id', 'org_id', 'secret_token']

    try:
        # Map credentials, replace defaults with ones from arguments
        for key in credential_keys:
            if arguments[key]:
                credentials[key] = arguments[key]
            else:
                credentials[key] = default_credentials[key]

            # Make sure key is not empty
            if not credentials[key]:
                logging.error('Credential ' + key + ' is empty!')
                exit(1)

    except KeyError, e:
        logging.error('Missing credential: %s' % str(e))
        exit(1)

    return credentials


def make_request(credentials, branch=None):
    """
    Makes the request to the Opbeat intake
    """
    url = 'https://intake.opbeat.com/api/v1/organizations/{0}/apps/{1}/releases/'.format(
        credentials['org_id'],
        credentials['app_id']
    )

    data = {
        'status': 'completed',
        'rev': get_data_from_git('git log -n 1 --pretty=format:%H'),
    }

    if branch is not None:
        data['branch'] = branch
    else:
        data['branch'] = get_data_from_git('git rev-parse --abbrev-ref HEAD')

    payload = json.dumps(data)

    request = urllib2.Request(
        url,
        headers={
            "Authorization": 'Bearer {0}'.format(credentials['secret_token']),
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": "{0}/1".format(package_name),
        },
        data=payload
    )

    try:
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.HTTPError, e:
        logging.error('An error occurred! Response from Opbeat: ' + str(e))
    except urllib2.URLError, e:
        logging.error('There is a problem with the URL: ' + str(e))


def main():
    parser = argparse.ArgumentParser(
        description='This script tracks release to Opbeat.com'
    )
    parser.add_argument('--version', action='version',
                        version='{0} {1}'.format(package_name, __version__)
                        )
    # parser.add_argument('-v', action='store_true', dest='verbose',
    #                     help='Enables verbose mode (not implemented)')
    parser.add_argument('-o', action='store', dest='org_id',
                        help='Organization ID from Opbeat app')
    parser.add_argument('-a', action='store', dest='app_id',
                        help='App ID from Opbeat app')
    parser.add_argument('-s', action='store', dest='secret_token',
                        help='Secret token from Opbeat app')
    parser.add_argument('-b', action='store', default=None, dest='branch',
                        help='Set branch name or disable by setting it to ""')

    args = parser.parse_args()
    arguments = vars(args)

    credentials = parse_credentials(arguments)

    response = make_request(
        credentials,
        branch=arguments['branch'],
    )

    print 'Response from Opbeat: '
    print response
