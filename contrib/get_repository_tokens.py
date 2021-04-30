#!/usr/bin/env python

import httplib2
import re
import json
import sys
import getopt
 
 
h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)

def get_rels(response):
    links = response["link"].split(',')
    regex = re.compile(r'<(.*?)>; rel="(\w+)"')
    rels_hash = {}
    for link in links:
        href, name = regex.findall(link)[0]
        rels_hash[name] = href
    return rels_hash
                        

def get_token(match_repo_url):
    (resp, content) = h.request("https://scc.suse.com/connect/organizations/repositories", "GET", headers={'Accept':'application/vnd.scc.suse.com.v4+json','cache-control':'no-cache'})
    repositories = []


    while True:
        for repository in json.loads(content):
            if match_repo_url in repository['url'].split("?")[0]:
                #print repository['url'].split("?")[-1]+"\n\t is the token for repository URL:\n\t"+repository['url'].split("?")[0]+"\n"
                print repository['url'].split("?")[0]+","+repository['url'].split("?")[-1]
        rels = get_rels(resp)
        if not 'next' in rels:
            break
        (resp, content) = h.request(rels['next'], "GET")

def print_USAGE():
    print 'Usage:'
    print '\t'+self+' -u <username> -o <password> <part of repository URL> [... <part of repository URL>]'
    print '\tUse the SCC mirror credentials of your organization for user and password'
    print '\tProvide strings to match against repository URL'
    print '\tThe script provides all matches, one per line, full URL and TOKEN separated by ",".'

def main(argv):
    user = ''
    password = ''
    try:
        opts, args = getopt.getopt(argv,"u:p:h",["user=","password=","help"])
    except getopt.GetoptError:
        print_USAGE()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print_USAGE()
            sys.exit()
        elif opt in ("-u", "--user"):
            user = arg
        elif opt in ("-p", "--password"):
            password = arg
    if not user or not password:
        print 'ERROR: missing user or password of your mirror credentials'
        print_USAGE()
        sys.exit()
    if not args:
        print 'ERROR: no strings to match against repository URL'
        print_USAGE()
        sys.exit()

    h.add_credentials(user, password)
    for match_repo_url in args:
        print match_repo_url
        get_token(match_repo_url)
 

if __name__ == "__main__":

    self= sys.argv[0]
    main(sys.argv[1:])