# patterns/observer.py
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, event_data):
        for observer in self._observers:
            observer.update(event_data)

class LoggerObserver:
    def update(self, event_data):
        print(f"[LOG] Event triggered: {event_data}")