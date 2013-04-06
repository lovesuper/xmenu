xmenu
=====
pre-alpha version 0.0.1

Simple console menu

EXAMPLE
=======

class Twitter(Item):
    ''' It twitt us as more as it can'''

    def __call__(self):
        sys.stdout.write('{0}\n'.format(self.name))


class Multiplier(Item):
    ''' Printing '''

    def __call__(self):
        sys.stdout.write('Lorem ipsum Labor Excepteur ea ut.')


def func():
    ''' I am a function. Tasty and fragrand.'''

    print 'This is it.'


class MyApp(App):
    ''' This is my App'''

    def __init__(self):

        menu = Menu(name='Main menu')
        menu.add(Twitter(name='Project run'), color='red')
        menu.add(Twitter(name='Other'))
        math = Menu(name='Math')
        math.add(Multiplier(name='Multi'), color='underline')
        inc_menu = Menu(name='Database')
        inc_menu.add(math)
        inc_menu.add(Twitter(name='ECreate'))
        inc_menu.add(Twitter(name='Drop'))
        menu.add(inc_menu)
        functinons = Menu(name='functinons', doc='Useful functions!')
        functinons.add(func, name='f')
        menu.add(functinons, color='underline')
        super(MyApp, self).__init__(menu=menu, stdout=sys.stdout)


def main():
    MyApp().run()

if __name__ == '__main__':
    main()
