# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['SecretSanta']

# Cell
import pandas as pd
from pathlib2 import Path
from configparser import ConfigParser
from .lottery import *
from .replace import *
from .email import *
from .constants import *
import numpy as np
import time

# Cell
class SecretSanta:
    '''
    Create and send emails in the name of Secret Santa.
    '''
    def __init__(self, sender_name, sender_email, subject, path, verbose = False):
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.subject = subject
        self.n_max = 10000
        self.path = path
        self.__read_inputs(path, verbose)
        self.__shuffle(verbose)
        self.__create_emails(path, verbose)

    def __read_inputs(self, path, verbose = False):
        self.__read_config(path)
        self.__read_participants(path, verbose)
        self.__read_replacements(path)
        self.__read_rules(path)

    def __read_config(self, path):
        # TODO: add parameter verbose
        config = ConfigParser()
        cf_path = path / CONFIG_FN
        n = len(config.read(cf_path))
        if n < 1 :
            raise SystemExit(f'Error while reading config file - file not found: {cf_path.absolute()}')
        self.config = config

    def __read_participants(self, path, verbose = False):
        csv = path / PARTICIPANTS_FN
        try:
            # read all participants from csv, read only specified columns and trim spaces
            self.participants = pd.read_csv(
                csv,
                usecols = ['first_name', 'last_name', 'language', 'sex', 'email'],
                skipinitialspace=True,
                comment = '#'
            )
        except ValueError as e:
            raise SystemExit(f'Error while reading participants csv - {e}')
        except FileNotFoundError as e:
            raise SystemExit(f'Error while reading participants csv - file not found: {csv.absolute()}')
        if verbose:
            self.print_participants()

    def __read_replacements(self, path):
        #TODO: add parameter verbose
        csv = path / REPLACEMENTS_FN
        try:
            self.replacements = pd.read_csv(
                csv,
                usecols = ['variable', 'language', 'sex', 'replacement'],
                skipinitialspace=True
            )
        except ValueError as e:
            raise SystemExit(f'Error while reading replaements csv - {e}')
        except FileNotFoundError as e:
            raise SystemExit(f'Error while reading replacements csv - file not found: {csv.absolute()}')

    def __read_rules(self, path):
        # TODO: add parameter verbose
        rules = ConfigParser()
        rules.optionxform = str
        cf_path = path / RULES_FN
        rules.read(cf_path)
        self.rules = rules

    def __check_rules(self, verbose = False):
        check = True
        for sec in self.rules.sections():
            for opt in self.rules.options(sec):
                for val in self.rules.get(sec, opt).split(','):
                    val = val.strip()
                    for a in self.assignments:
                        if ((sec == 'must') and (a[0] == opt) and (a[1] != val)):
                            check =  False
                            if verbose:
                                print(f'Rule [{sec}] failed: {opt} --> {val}')
                        if ((sec == 'not') and (a[0] == opt) and (a[1] == val)):
                            check = False
                            if verbose:
                                print(f'Rule [{sec}] failed: {opt} --> {val}')
        return check

    def __shuffle(self, verbose = False):
        '''
        Assigns each participant another participant (no self assignments) as presentee.
        '''
        self.participants.first_name.values
        for i in range(self.n_max):
            self.assignments = get_assignemnts(self.participants.first_name.values)
            if (self.__check_rules(verbose)):
                return self.assignments
        raise Exception(f'No assignment found within {self.n_max} random trials. Check the number of participants and corresponding rules.')

    def __create_emails(self, path, verbose = False, out = None):
        '''
        For each participant an email message is created but not sent yet. Based on the participants,
        replacements (both read earlier from separate csv files) and html-template file within the directory
        `path`, the following tasks are performed:

        1. Loop over the participants
        2. Create a dictionary based on the replacements from csv file
        3. Add to entries to the replacements dictionary: PERSON and PRESENTEE to replace them by the
           corresponding first names
        4. Apply all text replacements, then create and add the email message to the list of email messages
        5. Save the generated email within directory `out` (backup to resend to single participants if necessary)
        '''
        if out is None:
            out = path
        self.emails = list()
        for idx, row in self.participants.iterrows():
            html_tpl = self.__read_html_tpl(path, row.language)
            d = self.__get_replacements(row.language, row.sex)
            d.update({'PERSON': row.first_name})
            d.update({'PRESENTEE': self.__get_presentee(row.first_name)})
            v = get_variables(html_tpl)
            missing = np.setdiff1d(list(v), list(d.keys()))
            if len(missing) > 0:
                raise SystemExit(f'No replacement found for {missing} within {(path / REPLACEMENTS_FN).absolute()}')
            html = replace_vars(html_tpl, d)
            email = create_html_message(f'{self.sender_name} <{self.sender_email}>', row.email, self.subject, html, '', image_path = path)
            self.emails.append(email)
            with open(out / f'message_{row.first_name}.msg', 'wb') as f:
                f.write(bytes(email))

    def __read_html_tpl(self, path, lang):
        html_tpl_fn = path / (HTML_TPL_BASE_FN + lang + '.html')
        try:
            f = open(html_tpl_fn)
            html_tpl = f.read()
        except FileNotFoundError as e:
            raise SystemExit(f'Error while reading temlate message ({lang}) - file not found: {html_tpl_fn.absolute()}')
        finally:
            f.close()
        return html_tpl

    def __get_replacements(self, language, sex):
        d = dict()
        for idx, row in self.replacements[(self.replacements.language == language) & (self.replacements.sex == sex)].iterrows():
            d.update({row.variable: row.replacement})
        return d

    def __get_presentee(self, person):
        for i in range(len(self.assignments)):
            if self.assignments[i][0] == person:
                return self.assignments[i][1]
        return None

    def print_participants(self):
        '''
        Print all participants with corresponding information (first/last name, language,
        gender, email address) read from csv.
        '''
        print('Participants:')
        print('-------------')
        for idx, row in self.participants.iterrows():
            print(f'{row.first_name} {row.last_name} ({row.language}, {row.sex}): {row.email}')
        print('-------------')

    def print_assignments(self):
        '''
        Print all participants together with the currently assigned presentees.
        '''
        print('Participants --> Presemtees:')
        print('----------------------------')
        for a in self.assignments:
            print(f'{a[0]} --> {a[1]}')
        print('----------------------------')

    def print_ladina_andreas_assignments(self):
        '''
        Print all participants together with the currently assigned presentees.
        '''
        print('Participants --> Presemtees:')
        print('----------------------------')
        for a in self.assignments:
            if ((a[0] == 'Andreas') or (a[0] == 'Ladina')):
                print(f'{a[0]} --> {a[1]}')
        print('----------------------------')

    def send_emails(self, sleep_sec = 5):
        '''
        Send the Secret Santa email messages to its recipients.
        '''
        server = self.config['smtp']['server']
        port = self.config['smtp']['port']
        user = self.config['smtp']['user']
        pwd = self.config['smtp']['password']
        for email in self.emails:
            send_smtp_email(server, port, user, pwd, email)
            time.sleep(sleep_sec)