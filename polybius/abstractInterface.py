
class AbstractInterface():


    def __init__(self):

        self._buttons = []
        self._textInputs = []

    def draw(self, screen):
        for b in self._buttons:
            b.draw(screen)
        for t in self._textInputs:
            t.draw(screen)

    def handleEvent(self, event):
        for b in self._buttons:
            b.handleEvent(event,lambda: None)
        for t in self._textInputs:
            t.handleEvent(event,lambda: None)
