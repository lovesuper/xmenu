import sys
import xmenu


class CommandOne(xmenu.Item):

    ''' CommandOne doc string '''

    def __call__(self):
        print 'CommandOne performed.'


class CommandTwo(xmenu.Item):

    ''' CommandTwo doc string '''

    def __call__(self):
        print 'CommandTwo performed.'


@xmenu.Item(name='myFunction', color='red')
def command_three():
    ''' I am a function. Tasty and fragrant.'''

    print 'command three performed!'


main_menu = xmenu.Menu(name='Main menu')
main_menu.add(
    CommandTwo(name='Project run', color='red'),
    CommandTwo(name='Other'),
    xmenu.Menu(name='included menu').add(
        CommandTwo(name='Project run2', color='blue'),
        CommandTwo(name='Other2'),
        xmenu.Menu(name='Third-party menu').add(
            CommandTwo(name='Project run3', color='red'),
            CommandTwo(name='Other3')
        ),
    ),
    command_three,
)


def main():
    xmenu.App(menu=main_menu, stdout=sys.stdout)()


if __name__ == '__main__':
    main()
