from threading import Thread


class MyThread(Thread):
    def __init__(self, name, target):
        Thread.__init__(self, name=name, target=target)
        self._return_value = None

    def run(self):
        if self._target is not None:
            self._return_value = self._target()

    def join(self) -> None:
        Thread.join(self)

    @property
    def return_value(self):
        return self.return_value