from time import sleep
from PIL import ImageGrab, ImageChops
import screeninfo
import typing as T
from screeninfo.common import Monitor

# Define the blue color range (adjust these values as needed)
EXPERIENCE_COLOR: T.Tuple[int, int, int] = (42, 99, 216)
EXPERIENCE_DIVIDER_COLOR: T.Tuple[int, int, int] = (155, 176, 237)
DARK_BLUE_COLOR: T.Tuple[int, int, int] = (0, 34, 64)
LIGHT_BLUE_COLOR: T.Tuple[int, int, int] = (153, 166, 192)

DEAD_PLAYER_THRESHOLD = 70.0
SLEEP_TIME = 1

class XPBar:
    def __init__(self, left: int, top: int, right: int, bottom: int) -> None:
        self.xp_bar_location: T.Tuple[int, int, int, int] = (left, top, right, bottom)
        self.get_xp_bar()
        self.get_left_padding()
    
    def calculate_exp(self) -> int:
        self.max_experience_length: int = self.width - (self.left_padding * 2)
        self.actual_experience_length: int = 0
        for x in range(self.left_padding, self.width - self.left_padding):
            pixel: T.Tuple[int, int, int] = self.pixels[x, self.height // 2]
            if pixel == EXPERIENCE_COLOR or pixel == EXPERIENCE_DIVIDER_COLOR:
                self.actual_experience_length += 1

        return self.actual_experience_length / self.max_experience_length
        
    def get_xp_bar(self) -> None:
        self.width: int
        self.height: int

        self.xp_bar_image: ImageGrab.Image = ImageGrab.grab(self.xp_bar_location)
        self.width, self.height = self.xp_bar_image.size
        self.pixels: T.Any = self.xp_bar_image.load()

    def get_left_padding(self) -> None:
        left_padding: int = 0
        middle: int = self.height // 2
        for x in range(0, self.width):
            if self.pixels[x, middle] != DARK_BLUE_COLOR:
                left_padding = x
                break
            elif self.pixels[x, middle] == LIGHT_BLUE_COLOR:
                left_padding = 2  # We didn't find any experience on the bar, default to 2
                break

        self.left_padding: int = left_padding

    @classmethod
    def from_screenshot(cls, screenshot: ImageGrab.Image) -> "XPBar":
        width: int
        height: int
        width, height = screenshot.size
        pixels: T.Any = screenshot.load()

        # Find the bottom of the XP bar
        bottom: T.Optional[int] = None
        x: int = width // 2
        for y in range(height - 1, -1, -1):
            if pixels[x, y] == DARK_BLUE_COLOR or pixels[x, y] == LIGHT_BLUE_COLOR:
                bottom = y
                break

        if bottom is None:
            raise ValueError("XP bar not found")

        # Find the left and right bounds of the XP bar
        left: T.Optional[int] = None
        right: T.Optional[int] = None
        for x in range(width):
            if pixels[x, bottom] == DARK_BLUE_COLOR:
                left = x
                break
        
        for x in range(width - 1, 0, -1):
            if pixels[x, bottom] == DARK_BLUE_COLOR:
                right = x
                break

        if left is None or right is None:
            raise ValueError("XP bar bounds not found")

        # Find the top of the XP bar
        top: T.Optional[int] = None
        for y in range(bottom, 0, -1):
            if pixels[left, y] != DARK_BLUE_COLOR:
                top = y + 1
                break

        if top is None:
            raise ValueError("XP bar top not found")

        return cls(left, top, right + 1, bottom + 1)


class MonitorHandler:

    def __init__(self) -> None:
        self.monitors: T.List[Monitor] = screeninfo.get_monitors()
        self.screen: Monitor = next((monitor for monitor in self.monitors if monitor.is_primary), None)
        if self.screen is None:
            raise ValueError("No primary monitor found. Exiting.")

    def get_dimensions(self) -> tuple:
        return self.screen.width, self.screen.height
    
    def get_height_bounding_box(self, height: int) -> tuple:
        # Return a bounding box that is 100% width and height pixels from the bottom
        return 0, self.screen.height - height, self.screen.width, self.screen.height
    
    def print_monitors(self) -> None:
        for i, mon in enumerate(self.monitors):
            print(f"Monitor {i}: {mon.name}, Width: {mon.width}, Height: {mon.height}, Primary: {mon.is_primary}")

def capture_initial_screenshot(monitor: MonitorHandler) -> ImageGrab.Image:
    # Define the bounding box for the XP bar region (adjust these values as needed)
    bbox = (0, 0,  monitor.screen.width, monitor.screen.height)
    return ImageGrab.grab(bbox)

def main() -> int:
    monitor = MonitorHandler()
    screenshot = capture_initial_screenshot(monitor)

    xp_bar = XPBar.from_screenshot(screenshot)
    initial_xp: float = xp_bar.calculate_exp()
    print(f"Initial Experience: {initial_xp * 100:.2f}%")
    print('To exit the program, press Ctrl+C')
    try:
        while True:
            xp_bar.get_xp_bar()
            current_xp: float = xp_bar.calculate_exp()
            if current_xp > initial_xp:
                xp_gained: float = (current_xp - initial_xp) * 100
                if xp_gained > DEAD_PLAYER_THRESHOLD:  # player probably died, reset initial experience
                    initial_xp = current_xp
                    print(f"You Died. Current Experience: {current_xp * 100:.2f}%")
                else:
                    kills_to_level: float = (100 - initial_xp) / xp_gained
                    print(f"Gained Experience: {xp_gained:.2f}% - Kills to level: {kills_to_level:.2f}")
                    initial_xp = current_xp
            elif current_xp < initial_xp:
                xp_lost: float = (initial_xp - current_xp) * 100
                print(f"You Died. Lost Experience: {xp_lost * 100:.2f}%")
                initial_xp = current_xp
                
            sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        print("Exiting...")
        return 0

if __name__ == "__main__":
    main()
