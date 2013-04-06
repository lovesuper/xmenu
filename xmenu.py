# -*- coding: utf-8 -*-
import sys
from inspect import getdoc
from abc import ABCMeta, abstractmethod
# it takes Cmd2
from cmd2 import Cmd


def _history():
    ''' `Static` function for stack history '''
    _history.stack = list()
    _history.backward = lambda: (_history.stack.pop(),_history.stack.pop())
    while(True): _history.stack.append((yield))

_hist = _history()
next(_hist)


class Item(str):
    ''' Class that presents simple menu item '''

    __metaclass__ = ABCMeta

    def __new__(cls, name, *args, **kwargs):
        return str.__new__(cls, name)

    def __init__(self, name, *args, **kwargs):
        self.name = name

    @abstractmethod
    def __call__(self):
        pass


class Menu(dict):
    ''' Class that represents '''

    codes = {
        'bold': {True: '\x1b[1m', False: '\x1b[22m'},
        'cyan': {True: '\x1b[36m', False: '\x1b[39m'},
        'blue': {True: '\x1b[34m', False: '\x1b[39m'},
        'red': {True: '\x1b[31m', False: '\x1b[39m'},
        'magenta': {True: '\x1b[35m', False: '\x1b[39m'},
        'green': {True: '\x1b[32m', False: '\x1b[39m'},
        'underline': {True: '\x1b[4m', False: '\x1b[24m'}
    }

    def __init__(self, name='MenuItem', doc=None, *args, **kwargs):
        self.name = name
        self.__doc__ = doc or 'No doc'
        dict.__init__(self, *args)

    def __str__(self):
        return self.name

    def __call__(self):
        App(menu=self, stdout=sys.stdout).run()

    def add(self, item, name='Unknown item', color='green', doc=None):
        if not hasattr(item, 'name'):
            item.name = name

        item.__doc__ = doc or 'No doc.'
        item.color = color
        item.name = self.colorize(item.name, item.color)
        setattr(self, item.name, item)
        super(Menu, self).update({item.name: item})

    def colorize(self, val, color):
        return self.codes[color][True] + val + self.codes[color][False]


class App(Cmd, object):
    ''' This is the test of doc'''

    prompt = '>> '

    def __init__(self, menu, stdout):
        Cmd.__init__(self, 'tab', stdin=sys.stdin, stdout=sys.stdout)
        self.stdout = stdout or sys.stdout
        self.menu = menu
        if _history.stack:
            self.menu.add(self.Back(name='Back'), color='bold')

        self.menu.add(lambda: sys.exit('Bye.'),
                     name='Exit',
                     color='bold',
                     doc='Exit from programm.'
        )
        self.menu.add(self.Help(name='Help', app=self), color='bold')

        _hist.send(self.menu)

    class Help(Item):
        ''' Getting help.'''

        def __init__(self, name, app):
            delimiter = '-' * 55
            self.doc = delimiter
            self.doc += '\n App : {0}'.format(
                getdoc(app.__class__) or 'No doc.\n'
            )
            for key, obj in app.menu.items():
                doc = getdoc(app.menu[key])
                self.doc += '\n {0} : {1}'.format(key, doc)

            self.doc += '\n{0}\n'.format(delimiter)
            Item.__init__(self, name, app)

        def __call__(self):
            sys.stdout.write(str(self.doc) + '\n')

    class Back(Item):
        ''' Move into parent menu.'''

        def __init__(self, name, *args, **kwargs):
            Item.__init__(self, name, *args, **kwargs)

        def __call__(self):
            __, menu = _history.backward()
            App(menu=menu, stdout=sys.stdout).run()

    def select(self, variants, string):
        return self.menu[Cmd.select(self, variants, string)]

    def _output(self, output):
        self.stdout.write('{0}\n'.format(output))

    def run(self):
        ''' Run apps loop'''

        self._output(self.menu.name.upper())
        try:
            item = self.select(sorted(self.menu, reverse=True), self.prompt)
        except IndexError:
            self._output('No such command!')
        except KeyboardInterrupt:
            sys.exit('\nbye.')
        else:
            item()
        self.run()
