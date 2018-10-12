#!/usr/bin/env python

import click
import boto3
import time, datetime

@click.command()
@click.option('--profile','-p',help='aws profile',required=True)
@click.option('--message', '-m',help='event message',required=True)
@click.option('--group', '-g', help='log group name', required=True)
@click.option('--stream', '-s', help='stream name', required=True)
def main(profile, message, group, stream):

    session = boto3.session.Session(profile_name=str(profile))
    client = session.client('logs')

    timestamp = int(time.time()*1000)

    response = client.describe_log_streams(
        logGroupName=str(group),
        logStreamNamePrefix=str(stream),
        orderBy='LogStreamName',
        descending=True
    )

    print(response)

    print(response['logStreams'][0]['uploadSequenceToken'])
    next_token = str(response['logStreams'][0]['uploadSequenceToken'])

    response = client.put_log_events(
        logGroupName=str(group),
        logStreamName=str(stream),
        logEvents=[
            {
                'timestamp':timestamp,
                'message': str(message)
            },
        ],
        sequenceToken=next_token
    )

if __name__ == "__main__":
    main()
