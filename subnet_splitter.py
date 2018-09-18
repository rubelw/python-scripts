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
    print('Available ranges: '+str(s.get_available_ranges()))

    loop_count=0
    flag=False
    suffix=int(suffix)+1

    while not flag:

        try:
            loop_count+=1
            subnets = s.get_subnet(suffix, count=int(number_of_subnets))

            for subnet in subnets:
                print(subnet)
            flag = True

        except:
            suffix=int(suffix)+1

            if loop_count>25:
                flag=True
                print('can not determine subnets')

if __name__ == "__main__":
    main()


