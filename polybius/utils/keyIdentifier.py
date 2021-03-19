import pygame, string
from polybius.utils import EventWrapper 

class KeyIdentifier():

    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        """Used to obtain a singleton instance"""
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._KI()
        return cls._INSTANCE

    class _KI():
        #TO-DO: Caps Lock and Num Lock checks do no work quite right

        def __init__(self):

            self._numSymbols = ")!@#$%^&*("

            self._symbolKeys = [ord(p) for p in string.punctuation]

            self._symbols = {EventWrapper(pygame.KEYDOWN, i+48, [pygame.KMOD_SHIFT]):s
                               for i, s in enumerate(")!@#$%^&*(")}

            for x in range(10):
                self._symbols[EventWrapper(pygame.KEYDOWN, x+48)] = str(x)
                self._symbols[EventWrapper(pygame.KEYDOWN, x+256,
                                           [pygame.KMOD_NUM])] = str(x)

            for x in range(27):
                self._symbols[EventWrapper(pygame.KEYDOWN, x+97)] = chr(x+97)
                self._symbols[EventWrapper(pygame.KEYDOWN, x+97, [pygame.KMOD_SHIFT])] = chr(x+65)
                self._symbols[EventWrapper(pygame.KEYDOWN, x+97, [pygame.KMOD_CAPS])] = chr(x+65)
                
            self._symbols[EventWrapper(pygame.KEYDOWN, 91)] = "["
            self._symbols[EventWrapper(pygame.KEYDOWN, 92)] = "\\"
            self._symbols[EventWrapper(pygame.KEYDOWN, 93)] = "]"
            
            self._symbols[EventWrapper(pygame.KEYDOWN, 44)] = ","
            self._symbols[EventWrapper(pygame.KEYDOWN, 46)] = "."
            self._symbols[EventWrapper(pygame.KEYDOWN, 47)] = "/"
            self._symbols[EventWrapper(pygame.KEYDOWN, 59)] = ";"
            self._symbols[EventWrapper(pygame.KEYDOWN, 39)] = "'"
            self._symbols[EventWrapper(pygame.KEYDOWN, 96)] = "`"
            self._symbols[EventWrapper(pygame.KEYDOWN, 61)] = "="
            self._symbols[EventWrapper(pygame.KEYDOWN, 45)] = "-"
            
            self._symbols[EventWrapper(pygame.KEYDOWN, 44, [pygame.KMOD_SHIFT])] = "<"
            self._symbols[EventWrapper(pygame.KEYDOWN, 46, [pygame.KMOD_SHIFT])] = ">"
            self._symbols[EventWrapper(pygame.KEYDOWN, 47, [pygame.KMOD_SHIFT])] = "?"
            self._symbols[EventWrapper(pygame.KEYDOWN, 91, [pygame.KMOD_SHIFT])] = "{"
            self._symbols[EventWrapper(pygame.KEYDOWN, 93, [pygame.KMOD_SHIFT])] = "}"
            self._symbols[EventWrapper(pygame.KEYDOWN, 61, [pygame.KMOD_SHIFT])] = "+"
            self._symbols[EventWrapper(pygame.KEYDOWN, 96, [pygame.KMOD_SHIFT])] = "~"
            self._symbols[EventWrapper(pygame.KEYDOWN, 92, [pygame.KMOD_SHIFT])] = "|"
            self._symbols[EventWrapper(pygame.KEYDOWN, 39, [pygame.KMOD_SHIFT])] = '"'
            self._symbols[EventWrapper(pygame.KEYDOWN, 59, [pygame.KMOD_SHIFT])] = ":"
            self._symbols[EventWrapper(pygame.KEYDOWN, 45, [pygame.KMOD_SHIFT])] = "_"

            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_PLUS)] = "+"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_MINUS)] = "-"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_DIVIDE)] = "/"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_MULTIPLY)] = "*"
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_KP_PERIOD)] = "."
            self._symbols[EventWrapper(pygame.KEYDOWN, pygame.K_SPACE)] = " "

            self._wrappers = [w for w in self._symbols.keys()]
            self._wrappers.sort(key=lambda x: len(x.getMods()))
            self._wrappers.reverse()

        def getChar(self, event):     
            for wrapper in self._wrappers:
                if wrapper.check(event):
                    return self._symbols[wrapper]
            return ""

KEY_IDENTIFIER = KeyIdentifier.getInstance()
