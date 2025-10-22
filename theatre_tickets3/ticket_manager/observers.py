# ticket_manager/observers.py
class Observer:
    def update(self, message):
        pass


class EmailNotifier(Observer):
    def update(self, message):
        print(f"[EMAIL] {message}")


class AdminNotifier(Observer):
    def update(self, message):
        print(f"[ADMIN] {message}")


class BookingSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)
