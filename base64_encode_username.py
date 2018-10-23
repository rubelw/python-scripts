#!/usr/bin/env python

import click
import base64



@click.command()
@click.option('--username','-u',help='username',required=True)
@click.option('--password', '-p',help='password',required=True)
def main(username, password):

    userPass = str(username)+':'+str(password)
    userPass = userPass.encode("utf-8")
    base64string = base64.b64encode(userPass).decode("utf-8")
    print('base64 encrypted header: '+str(base64string))


if __name__ == "__main__":
    main()


