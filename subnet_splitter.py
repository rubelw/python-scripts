#!/usr/bin/env python

import click
from netaddr import IPNetwork, cidr_merge, cidr_exclude


class IPSplitter(object):
    def __init__(self, base_range):
        self.avail_ranges = set((IPNetwork(base_range),))

    def get_subnet(self, prefix, count=None):
        for ip_network in self.get_available_ranges():
            subnets = list(ip_network.subnet(prefix, count=count))
            if not subnets:
                continue
            self.remove_avail_range(ip_network)
            self.avail_ranges = self.avail_ranges.union(set(cidr_exclude(ip_network, cidr_merge(subnets)[0])))
            return subnets

    def get_available_ranges(self):
        return sorted(self.avail_ranges, key=lambda x: x.prefixlen, reverse=True)

    def remove_avail_range(self, ip_network):
        self.avail_ranges.remove(ip_network)


@click.command()
@click.option('--cidr','-c',help='cidr block',required=True)
@click.option('--number-of-subnets', '-s',help='number of subnets',required=True)
def main(cidr,number_of_subnets):
    print("I'm a beautiful CLI ✨")
    s = IPSplitter(cidr)
    (prefix,suffix) = cidr.split('/')
    print('prefix: '+str(prefix))
    print('suffix: '+str(suffix))
    print(s.get_available_ranges())

    print(s.get_subnet(int(suffix)+2, count=int(number_of_subnets)))

if __name__ == "__main__":
    main()


