# -*- coding: utf-8 -*-

__author__ = "Esteban Barón"
__copyright__ = "Copyright 2020, Esteban Barón ,EBP"
__license__ = "MIT"
__email__ = "esteban@gominet.net"
__status__ = "Beta"
__version__ = "0.1.0b1"

from SAlogger import SAlogger
from SAconfig import SAconfig
import getpass
import requests
from bs4 import BeautifulSoup
import base64
# import xml.etree.ElementTree as ET
import defusedxml.ElementTree as ET
import boto3
import os
from pathlib import Path
import configparser
import logging


class SAsamlaws(SAlogger):

    _MSG = (
        'Inicio samlaws',
        'Config: {0}',
        'Formdata: {0}',
        'Faltan datos requeridos',
        'Session response: {0}',
        'Respuesta no contiene un SAML assertion valido'
        )

    def __init__(self, configpath=None, home=None):
        SAlogger.__init__(self)
        logging.basicConfig(level='DEBUG')
        self._logger.setLevel('DEBUG')
        self.debug(0)
        if home is None:
            home = str(Path.home())
        defaults = {
            'region': 'eu-west-1',
            'outputformat': 'json',
            'username': None,
            'password': None,
            'sslverification': True,
            'idpentrydomain': None,
            'idpentryurl': str(
                '/adfs/ls/IdpInitiatedSignOn.aspx?' +
                'loginToRp=urn:amazon:webservices'),
            'role': None,
            'awsconfigfile':
                home +
                os.path.sep +
                '.aws' +
                os.path.sep +
                'credentials',
            'sessionseconds': 3600}
        config = SAconfig(configpath).load_cfg(defaults)
        # Valores por defecto
        self._config = config

    def formdata(self):
        # Get the federated credentials from the user
        res = {}
        res['Username'] = self._config['username']
        if res['Username'] is None:
            print('Username:', end=' ')
            res['Username'] = str(input())   # nosec
        res['Password'] = self._config['password']
        if res['Password'] is None:
            res['Password'] = getpass.getpass()
        res['AuthMethod'] = 'FormsAuthentication'
        return res

    def showconfig(self):
        return self._config

    def getRoles(self, assertion):
        # Parse the returned assertion and extract the authorized roles
        roles = []
        principals = []
        rolecomp = self._config['role']
        root = ET.fromstring(base64.b64decode(assertion))
        xpath = ("./{0}Assertion/{0}AttributeStatement/"
                 "{0}Attribute[@Name='{1}']/").format(
                      '{urn:oasis:names:tc:SAML:2.0:assertion}',
                      'https://aws.amazon.com/SAML/Attributes/Role')

        for element in root.findall(xpath):
            # Note the format of the attribute value should be
            # role_arn,principal_arn, but lots of blogs list it
            # as principal_arn,role_arn so let's reverse
            # them if needed
            chunks = element.text.split(',')
            rolidx = 0
            principalidx = 1
            if 'saml-provider' in chunks[0]:
                rolidx = 1
                principalidx = 0
            if rolecomp is not None and chunks[rolidx] == rolecomp:
                return ([chunks[rolidx]], [chunks[principalidx]])
            roles.append(chunks[rolidx])
            principals.append(chunks[principalidx])

        return (roles, principals)

    def _checkawsconfigfile(self):
        # Antes de hacer nada más,
        # compruebo si existe los directorios en el que se
        # pondrá el resultado.
        if not os.path.isfile(self._config['awsconfigfile']):
            tmppath = Path(self._config['awsconfigfile'])
            if not os.path.isdir(tmppath.parent):
                os.mkdir(tmppath.parent)

    def main(self):
        ret = 0
        self.debug(1, str(self._config))
        formdata = self.formdata()
        self.debug(2, str(formdata))

        self._checkawsconfigfile()

        session = requests.Session()

        # Opens the initial AD FS URL and follows all of the HTTP302 redirects
        idpentrydomain = self._config['idpentrydomain']
        idpentryurl = self._config['idpentryurl']
        if not idpentrydomain or not idpentryurl:
            self.error(3)
            ret = 1
            return ret
        response1 = session.get(
            idpentrydomain + idpentryurl,
            verify=self._config['sslverification'])
        self.debug(4, str(response1))

        soup1 = BeautifulSoup(response1.text, features="html.parser")
        idpentryurl = soup1.find('form').get('action')

        response2 = session.post(
            idpentrydomain + idpentryurl,
            formdata,
            verify=self._config['sslverification'])
        self.debug(4, str(response2))

        # Decode the response and extract the SAML assertion
        soup2 = BeautifulSoup(response2.text, features="html.parser")
        assertion = ''

        # Look for the SAMLResponse attribute of the input tag (determined by
        # analyzing the debug print lines above)
        for inputtag in soup2.find_all('input'):
            if(inputtag.get('name') == 'SAMLResponse'):
                # print(inputtag.get('value'))
                assertion = inputtag.get('value')

        # Better error handling is required for production use.
        if (assertion == ''):
            # TODO: Insert valid error checking/handling
            self.info(5)
            ret = 2
            return ret

        # Parse the returned assertion and extract the authorized roles
        roles, principals = self.getRoles(assertion)

        self._logger.debug("Los roles: {0}".format(str(roles)))

        # If I have more than one role, ask the user which one they want,
        # otherwise just proceed
        lenroles = len(roles)
        if lenroles > 1:
            i = 0
            print("Please choose the role you would like to assume:")
            for role in roles:
                print('[', i, ']: ', role)
                i += 1

            print("Selection: ", end=' ')

            selectedroleindex = input()   # nosec

            # Basic sanity check of input
            if int(selectedroleindex) > (lenroles - 1):
                print('You selected an invalid role index, please try again')
                ret = 3
                return ret

            role_arn = roles[int(selectedroleindex)]
            principal_arn = principals[int(selectedroleindex)]

        else:
            role_arn = roles[0]
            principal_arn = principals[0]

        self._logger.debug("role_arn {0} principal_arn {1}"
                           .format(role_arn, principal_arn))

        # Use the assertion to get an AWS STS token using Assume Role with SAML
        # conn = boto.sts.connect_to_region(region)
        conn = boto3.client('sts', region_name=self._config['region'])
        token = conn.assume_role_with_saml(
            RoleArn=role_arn,
            PrincipalArn=principal_arn,
            SAMLAssertion=assertion,
            DurationSeconds=int(self._config['sessionseconds']))

        # Read in the existing config file
        awsconfig = configparser.RawConfigParser()
        awsconfig.read(self._config['awsconfigfile'])

        # Put the credentials into a saml specific section
        # instead of clobbering the default credentials
        if not awsconfig.has_section('saml'):
            awsconfig.add_section('saml')

        awsconfig.set('saml', 'output', self._config['outputformat'])
        awsconfig.set('saml', 'region', self._config['region'])
        awsconfig.set('saml',
                      'aws_access_key_id',
                      token['Credentials']['AccessKeyId'])
        awsconfig.set('saml',
                      'aws_secret_access_key',
                      token['Credentials']['SecretAccessKey'])
        awsconfig.set('saml',
                      'aws_session_token',
                      token['Credentials']['SessionToken'])

        # Write the updated config file
        with open(self._config['awsconfigfile'], 'w+') as configfile:
            awsconfig.write(configfile)

        return ret


def main(configpath=None, home=None):
    objexec = SAsamlaws(configpath, home)
    return objexec.main()
# end def main


if __name__ == "__main__":
    print("Este fichero pertenece a un módulo, "
          "no es operativo como aplicación independiente.")
