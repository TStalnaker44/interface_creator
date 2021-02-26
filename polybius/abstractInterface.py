
class AbstractInterface():


    def __init__(self):

        self._buttons = []

    def draw(self, screen):
        for b in self._buttons:
            b.draw(screen)

    def handleEvent(self, event):
        for b in self._buttons:
            b.handleEvent(event,lambda: None)
