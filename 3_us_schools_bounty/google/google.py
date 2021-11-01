import sys

from googlesearch import search, get_random_user_agent

# TODO port to argparse
from optparse import OptionParser, IndentedHelpFormatter


class BannerHelpFormatter(IndentedHelpFormatter):

    "Just a small tweak to optparse to be able to print a banner."

    def __init__(self, banner, *argv, **argd):
        self.banner = banner
        IndentedHelpFormatter.__init__(self, *argv, **argd)

    def format_usage(self, usage):
        msg = IndentedHelpFormatter.format_usage(self, usage)
        return '%s\n%s' % (self.banner, msg)


def main():

    # Parse the command line arguments.
    formatter = BannerHelpFormatter(
        "Python script to use the Google search engine\n"
        "By Mario Vilas (mvilas at gmail dot com)\n"
        "https://github.com/MarioVilas/googlesearch\n"
    )
    parser = OptionParser(formatter=formatter)
    parser.set_usage("%prog [options] query")
    parser.add_option(
        '--tld', metavar='TLD', type='string', default='com',
        help="top level domain to use [default: com]")
    parser.add_option(
        '--lang', metavar='LANGUAGE', type='string', default='en',
        help="produce results in the given language [default: en]")
    parser.add_option(
        '--tbs', metavar='TBS', type='string', default='0',
        help="produce results from period [default: 0]")
    parser.add_option(
        '--safe', metavar='SAFE', type='string', default='off',
        help="kids safe search [default: off]")
    parser.add_option(
        '--country', metavar='COUNTRY', type='string', default='',
        help="region to restrict search on [default: not restricted]")
    parser.add_option(
        '--num', metavar='NUMBER', type='int', default=10,
        help="number of results per page [default: 10]")
    parser.add_option(
        '--start', metavar='NUMBER', type='int', default=0,
        help="first result to retrieve [default: 0]")
    parser.add_option(
        '--stop', metavar='NUMBER', type='int', default=0,
        help="last result to retrieve [default: unlimited]")
    parser.add_option(
        '--pause', metavar='SECONDS', type='float', default=2.0,
        help="pause between HTTP requests [default: 2.0]")
    parser.add_option(
        '--rua', action='store_true', default=False,
        help="Randomize the User-Agent [default: no]")
    parser.add_option(
        '--insecure', dest="verify_ssl", action='store_false', default=True,
        help="Randomize the User-Agent [default: no]")
    (options, args) = parser.parse_args()
    query = ' '.join(args)
    if not query:
        parser.print_help()
        sys.exit(2)
    params = [
        (k, v) for (k, v) in options.__dict__.items()
        if not k.startswith('_')]
    params = dict(params)

    # Randomize the user agent if requested.
    if 'rua' in params and params.pop('rua'):
        params['user_agent'] = get_random_user_agent()

    # Run the query.
    for url in search(query, **params):
        print(url)
        try:
            sys.stdout.flush()
        except Exception:
            pass


if __name__ == '__main__':
    main()
    print("AAA")
