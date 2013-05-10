# -*- coding: utf-8 -*-
import sys
from cmd2 import Cmd
from inspect import getdoc

PROMPT = '>> '
DELIMITER = '-' * 55
COLORS = {
    'bold': {True: '\x1b[1m', False: '\x1b[22m'},
    'cyan': {True: '\x1b[36m', False: '\x1b[39m'},
    'blue': {True: '\x1b[34m', False: '\x1b[39m'},
    'red': {True: '\x1b[31m', False: '\x1b[39m'},
    'magenta': {True: '\x1b[35m', False: '\x1b[39m'},
    'green': {True: '\x1b[32m', False: '\x1b[39m'},
    'underline': {True: '\x1b[4m', False: '\x1b[24m'},
}


def history():
    ''' Static function for stack history '''

    history.stack = list()
    history.backward = lambda: (history.stack.pop(), history.stack.pop())
    while True:
        history.stack.append((yield))

stack = history()
next(stack)


def _colorize(string, color):
    color = COLORS[color]

    return color[True] + string + color[False]


class Item(str):

    ''' Class that presents simple menu item '''

    def __new__(cls, name=None, *args, **kw):
        return str.__new__(cls, name)

    def __init__(self, name=None, color='bold'):
        self.name = _colorize(name or self.__class__.__name__, color)
        self.__doc__ = self.__doc__ or 'No doc.'

    def __call__(self, func, *args, **kw):
        func.name = self.name

        return func


class Back(Item):

    ''' Move into parent menu.'''

    def __call__(self):
        __, prev_menu = history.backward()
        App(menu=prev_menu)()


class Help(Item):

        ''' Getting help.'''

        def __init__(self, name, color, app):
            self.doc = DELIMITER
            self.doc += '\n App : {0}'.format(
                getdoc(app.__class__) or 'No doc.\n'
            )
            for key, obj in app.menu.iteritems():
                self.doc += '\n{0} : {1}'.format(key, getdoc(app.menu[key]))

            self.doc += '\n{0}\n'.format(DELIMITER)
            Item.__init__(self, name, color)

        def __call__(self):
            sys.stdout.write(str(self.doc))


class Menu(dict):

    ''' Class that represents complex menu item'''

    def __init__(self, name='MenuItem', color='bold', doc=None, *args, **kw):
        self.name = _colorize(name, color)
        self.__doc__ = doc or 'No doc'
        dict.__init__(self, *args)

    def __str__(self):
        return self.name

    def __call__(self):
        App(menu=self)()

    def add(self, *items):
        map(lambda e: self.update({e.name: e}), items)

        return self


class App(Cmd, object):

    ''' This is the app template '''

    def __init__(self, menu):
        Cmd.__init__(self, 'tab', stdin=sys.stdin, stdout=sys.stdout)
        self.menu = menu

        @Item(name='Exit', color='bold')
        def Exit():
            sys.exit('bye.')

        self.menu.add(Exit, Help(name='Help', color='blue', app=self))
        if history.stack:
            self.menu.add(Back())

        stack.send(self.menu)

    def __call__(self):
        ''' Run apps loop'''
        self._output(self.menu.name)
        try:
            item = self.menu[self.select(sorted(self.menu, reverse=True),
                                         PROMPT)]
        except (KeyboardInterrupt, EOFError):
            sys.exit('\nbye.')
        except IndexError:
            self._output('No such command!')
        else:
            item()

        self()

    def _output(self, output):
        sys.stdout.write('{0}\n'.format(output))
