class Observable:
    def __init__(self):
        self._listeners = {}

    def on(self, event_name, listener):
        """Add a listener for an event."""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    def off(self, event_name, listener):
        """Remove event listener."""
        if event_name in self._listeners:
            self._listeners[event_name].remove(listener)

    def emit(self, event_name, *args, **kwargs):
        """Trigger an event."""
        if event_name in self._listeners:
            for listener in self._listeners[event_name]:
                listener(*args, **kwargs)
