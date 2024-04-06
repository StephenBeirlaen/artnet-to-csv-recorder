import time
from collections import deque


class FpsCalculator:
    def __init__(self):
        self.prev_frame_time = None
        self.new_frame_time = None
        self.last_frame_times = FrameTimeCollection(max_size=100)

    def start(self):
        self.prev_frame_time = time.time()

    def chrono(self):
        self.new_frame_time = time.time()
        elapsed_frame_time = self.new_frame_time - self.prev_frame_time
        self.prev_frame_time = self.new_frame_time

        self.last_frame_times.add_measurement(elapsed_frame_time)

    def calculate_average_fps(self) -> float:
        fps = 1.0 / self.last_frame_times.calculate_average()

        return fps


class FrameTimeCollection:
    def __init__(self, max_size):
        self.max_size = max_size
        self.queue = deque()

    def add_measurement(self, element):
        if len(self.queue) >= self.max_size:
            self.queue.popleft()  # Remove the oldest element

        self.queue.append(element)  # Add the new element

    def calculate_average(self) -> float:
        return sum(self.queue) / len(self.queue)
