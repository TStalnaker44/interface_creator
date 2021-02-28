
class AbstractInterface():


    def __init__(self):

        self._buttons = []
        self._textInputs = []
        self._textBoxes = []
        self._multiTextBoxes = []
        self._progressBars = []
        self._panels = []

    def getWidgets(self):
        return self._panels + self._buttons + self._textInputs + \
               self._textBoxes + self._multiTextBoxes +\
               self._progressBars

    def draw(self, screen):
        for w in self.getWidgets():
            w.draw(screen)

    def handleEvent(self, event):
        for b in self._buttons:
            b.handleEvent(event,lambda: None)
        for t in self._textInputs:
            t.handleEvent(event,lambda: None)

    def update(self, ticks):
        for t in self._textInputs:
            t.update(ticks)
