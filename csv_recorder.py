import csv
import os
from pathlib import Path


class CsvRecorder:
    def __init__(self, config):
        self.recording_dir = Path(config.get('recording_dir'))
        self.recording_save_path = None
        self.recorded_frames = None
        self.dmx_channels_to_record = None

        os.listdir(self.recording_dir)
        print(f"Access to '{self.recording_dir}' granted.")

    def start_recording(
        self,
        recording_name: str,
        dmx_channels_to_record: list
    ):
        if self.recording_save_path is not None:
            raise Exception('A recording has already been started')

        self.recording_save_path = str(self.recording_dir / (recording_name + '.csv'))
        self.recorded_frames = []
        self.dmx_channels_to_record = dmx_channels_to_record

        print(f"[CSV recorder] Started recording to {self.recording_save_path}")

    def record_frame(self, frame: list):
        if self.recording_save_path is None:
            # Don't record when it's not needed
            return

        self.recorded_frames.append(frame)

    def stop_recording(self):
        if self.recording_save_path is None:
            raise Exception('The last recording has already been stopped')

        with open(self.recording_save_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(
                csv_file,
                delimiter=',',
                quoting=csv.QUOTE_MINIMAL
            )

            # Write the header row (DMX channels)
            csv_writer.writerow(self.dmx_channels_to_record)

            # Write the data rows (DMX values)
            for frame in self.recorded_frames:
                csv_writer.writerow(frame)

        print(f"[CSV recorder] Stopped recording to {self.recording_save_path}")

        self.recording_save_path = None
        self.recorded_frames = None
        self.dmx_channels_to_record = None
