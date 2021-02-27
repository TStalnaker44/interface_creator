
class AbstractInterface():


    def __init__(self):

        self._buttons = []
        self._textInputs = []
        self._textBoxes = []

    def draw(self, screen):
        for b in self._buttons:
            b.draw(screen)
        for t in self._textInputs:
            t.draw(screen)
        for t in self._textBoxes:
            t.draw(screen)

    def handleEvent(self, event):
        for b in self._buttons:
            b.handleEvent(event,lambda: None)
        for t in self._textInputs:
            t.handleEvent(event,lambda: None)

    def update(self, ticks):
        for t in self._textInputs:
            t.update(ticks)
