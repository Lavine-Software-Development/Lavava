import sys
from pathlib import Path

# Get the directory containing your script or module
current_dir = Path(__file__).parent

# Get the parent directory
parent_dir = current_dir.parent

# Add the parent directory to sys.path
sys.path.append(str(parent_dir))

# Now you can import the module as if it was in the same directory
from track_change_decorator import track_changes

# Example usage adapted for simplified logic
class BaseObject:
    def __init__(self):
        self.tick_values = set()

# Example of using track_changes with a naming convention
@track_changes('tick_values', 'is_port', 'dynamic')
class WatchedObject(BaseObject):
    def __init__(self, is_port=None, dynamic=None, size=None, owner=None):
        self.size = size
        self.owner = owner
        super().__init__()

# Demonstration
watched_obj = WatchedObject(is_port=True, dynamic=False)
print(f"Initial tick_values: {watched_obj.tick_values}")

watched_obj.is_port = 'bean'
watched_obj.dynamic = True
watched_obj.size = 5
watched_obj.owner = "Player 1"
print(f"Modified tick_values: {watched_obj.tick_values}")

print(watched_obj.__is_port)

watched_obj.tick_values.clear()
print(f"Cleared tick_values: {watched_obj.tick_values}")