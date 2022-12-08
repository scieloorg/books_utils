#!/usr/bin/env python
import os
import requests
import argparse
import csv


def get_distinct_authors_total(api_host='localhost', api_port='5984', author_profile='all', publisher='all', distinct=True):
    try:

        resp = requests.get('http://{0}:{1}/scielobooks_1a/_design/scielobooks/_view/monographs_and_parts_visible?include_docs=true'.format(api_host, api_port))
    except:
        exit("API connection refused, please check the script configurations running ./{0} -h".format(os.path.basename(__file__)))

    jsondocs = resp.json()

    authors = set() if bool(distinct) else []

    # csv
    f = open('%s_%s.csv' % (publisher, author_profile), 'w')

    # create the csv writer
    writer = csv.writer(f, delimiter="|")
    for reg in jsondocs['rows']:  # rows e uma array (lista) de registros no JSON

        #Get the publisher form monograph or publisher
        try:
            regpub = reg['doc']['publisher']
        except KeyError:
            try:
                regpub = reg['doc']['monograph_publisher']
            except KeyError:
                continue

        # if a especific publisher
        if publisher != 'all':
            # if not the especif publisher pass
            if not regpub.lower() == publisher.lower():
                continue

        if 'creators' in reg['doc']:
            if len(reg['doc']['creators']) > 0:
                
                for creator_data in reg['doc']['creators']:

                    if creator_data[0][0] == 'role':
                        role = creator_data[0][1]

                    if creator_data[1][0] == 'full_name':
                        name = creator_data[1][1]

                    if author_profile == 'all':
                        if distinct: 
                            authors.add(name)
                        else:
                            authors.append(name)

                    elif role == author_profile:
                        if distinct: 
                            authors.add(name)
                        else:
                            authors.append(name)

                    # write a row to the csv file
                    writer.writerow([reg['doc']['_id'], regpub, name, author_profile])       

        if 'monograph_creators' in reg['doc']:
            if len(reg['doc']['monograph_creators']) > 0:

                for creator_data in reg['doc']['monograph_creators']:

                    if creator_data[0][0] == 'role':
                        role = creator_data[0][1]

                    if creator_data[1][0] == 'full_name':
                        name = creator_data[1][1]

                    if author_profile == 'all':
                        if distinct: 
                            authors.add(name)
                        else:
                            authors.append(name)

                    elif role == author_profile:
                        if distinct: 
                            authors.add(name)
                        else:
                            authors.append(name)
                
                    # write a row to the csv file
                    writer.writerow([reg['doc']['_id'], regpub, name, author_profile])       

    # close the file
    f.close()

    return len(authors)


def main(*args, **xargs):

    authors = get_distinct_authors_total(api_host=xargs['api_host'],
                                         api_port=int(xargs['api_port']),
                                         author_profile=xargs['author_profile'],
                                         publisher=xargs['publisher'],
                                         distinct=xargs['distinct'])

    print(authors)

parser = argparse.ArgumentParser(description="Create an access report")
parser.add_argument('--api_host', default='localhost', help='The CouchDB API hostname')
parser.add_argument('--api_port', default='5984', help='The CouchDB API port')
parser.add_argument('--author_profile', default='all', help='The author profile registered into database')
parser.add_argument('--publisher', default='all', help='The publisher value registered into database')
parser.add_argument('--distinct', dest='distinct', action='store_true', help='Contagem de forma distinta.')
args = parser.parse_args()

if __name__ == "__main__":

    main(api_host=args.api_host,
         api_port=args.api_port,
         author_profile=args.author_profile,
         publisher=args.publisher,
         distinct=args.distinct
         )
