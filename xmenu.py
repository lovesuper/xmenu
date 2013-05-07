# -*- coding: utf-8 -*-
import sys
from inspect import getdoc
from cmd2 import Cmd


def history():
    ''' Static function for stack history '''

    history.stack = list()
    history.backward = lambda: (history.stack.pop(),
                                history.stack.pop())
    while(True):
        history.stack.append((yield))

_hist = history()
next(_hist)


colors = {
    'bold': {True: '\x1b[1m', False: '\x1b[22m'},
    'cyan': {True: '\x1b[36m', False: '\x1b[39m'},
    'blue': {True: '\x1b[34m', False: '\x1b[39m'},
    'red': {True: '\x1b[31m', False: '\x1b[39m'},
    'magenta': {True: '\x1b[35m', False: '\x1b[39m'},
    'green': {True: '\x1b[32m', False: '\x1b[39m'},
    'underline': {True: '\x1b[4m', False: '\x1b[24m'},
}


def colorize(string, color):
    color = colors[color]
    return color[True] + string + color[False]


class Item(str):

    ''' Class that presents simple menu item '''

    def __new__(cls, name=None, *args, **kw):
        return str.__new__(cls, name)

    def __init__(self, name=None, color='bold'):
        if name is None:
            name = self.__class__.__name__
        self.name = name
        self.color = color

    def __call__(self, func, *args, **kw):
        func.name = self.name
        func.color = self.color
        return func


class Back(Item):

    ''' Move into parent menu.'''

    def __call__(self):
        __, menu = history.backward()
        App(menu=menu, stdout=sys.stdout)()


class Help(Item):

        ''' Getting help.'''

        def __init__(self, name, color, app):
            delimiter = '-' * 55
            self.doc = delimiter
            self.doc += '\n App : {0}'.format(
                getdoc(app.__class__) or 'No doc.\n'
            )
            for key, obj in app.menu.items():
                doc = getdoc(app.menu[key])
                self.doc += '\n {0} : {1}'.format(key, doc)

            self.doc += '\n{0}\n'.format(delimiter)
            Item.__init__(self, name, color)

        def __call__(self):
            sys.stdout.write(str(self.doc) + '\n')


class Menu(dict):

    ''' Class that represents complex menu item'''

    def __init__(self, name='MenuItem', color='bold', doc=None, *args, **kw):
        self.name = name
        self.color = color
        self.__doc__ = doc or 'No doc'
        dict.__init__(self, *args)

    def __str__(self):
        return self.name

    def __call__(self):
        App(menu=self, stdout=sys.stdout)()

    def add(self, *items):
        for item in items:
            item.__doc__ = item.__doc__ or 'No doc.'
            item.name = colorize(item.name, item.color)
            self.update({item.name: item})
        return self


class App(Cmd, object):

    ''' This is the app template '''

    prompt = '>> '

    def __init__(self, menu, stdout):
        Cmd.__init__(self, 'tab', stdin=sys.stdin, stdout=stdout)
        self.stdout = stdout or sys.stdout
        self.menu = menu
        if history.stack:
            self.menu.add(Back())

        @Item(name='Exit', color='bold')
        def Exit():
            sys.exit('bye.')

        self.menu.add(Exit)
        self.menu.add(Help(name='Help', color='blue', app=self))
        _hist.send(self.menu)

    def __call__(self):
        ''' Run apps loop'''

        self._output(self.menu.name.upper())
        try:
            item = self.select(sorted(self.menu, reverse=True), self.prompt)
        except IndexError:
            self._output('No such command!')
        except (KeyboardInterrupt, EOFError):
            sys.exit('\nbye.')
        else:
            item()
        self()

    def select(self, variants, string):
        return self.menu[Cmd.select(self, variants, string)]

    def _output(self, output):
        self.stdout.write('{0}\n'.format(output))
