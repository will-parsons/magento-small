#! /usr/bin/env python

import json
import re
import requests
import sys


class MagentoInteraction(object):
    def __init__(self, ip, domain="example.com"):
        self.ip = ip
        self.domain = domain[7:-1]
        self.session = requests.Session()
        self.session.headers.update({"Host": self.domain})


    def magento_get_home(self):
        url = "http://{}/".format(self.ip)
        print "url is {}".format(url)
        r = self.session.get(url, allow_redirects=False, verify=False)
        while r.is_redirect:
            redirect_url = r.headers.get('location')
            print redirect_url
            patched_url = re.sub(self.domain, self.ip, redirect_url)
            print "redirecting to {}...".format(patched_url)
            r = self.session.get(patched_url, allow_redirects=False, verify=False)
        print "status code is {}".format(r.status_code)
        return r.text

    def load_page(self):
        content = self.magento_get_home()
        return "Magento Demo Store. All Rights Reserved." in content


if __name__ == "__main__":
    print json.dumps(sys.argv)
    ip = sys.argv[1]
    domain = sys.argv[2]
    magento = MagentoInteraction(ip, domain=domain)

    if magento.load_page():
        print "Magento home page successful."
        sys.exit(0)
    else:
        print "failed to load home page :("
        sys.exit(1)
