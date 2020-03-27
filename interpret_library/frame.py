

class Frame :
    def __init__(self):
        super().__init__()
        self.globalFrame = {}
        self.tmpFrame = {}
        self.tmpFrameDefined = False
        self.frameStack = []

    def getFrame(self, frame: str) -> dict:
        if frame == 'GF':
            return self.globalFrame
        elif frame == 'LF':
            return (self.frameStack[-1] if len(self.frameStack) > 0 else None)
        elif frame == 'TF':
            return (self.tmpFrame if self.tmpFrameDefined else None)
        else:
            return None