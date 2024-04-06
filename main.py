import datetime
import uuid

import yaml
from sshkeyboard import listen_keyboard
from stupidArtnet import StupidArtnetServer
from tabulate import tabulate

from arguments_service import ArgumentsService
from channel_range_parser import ChannelRangeParser
from csv_recorder import CsvRecorder
from fps_calculator import FpsCalculator

dmx_data_indices_to_record = []
is_recording = False
recording_file_prefix = ''


def on_keypress(key):
    if key == 'r':
        global is_recording

        if is_recording is False:
            is_recording = True

            now = datetime.datetime.now()
            current_recording_name = f"{recording_file_prefix + ' - ' if recording_file_prefix != '' else ''}{now.strftime('%Y-%m-%d %H.%M.%S')} {str(uuid.uuid4())}"

            csv_recorder.start_recording(
                recording_name=current_recording_name,
                dmx_channels_to_record=dmx_channels_to_record,
            )
        elif is_recording is True:
            is_recording = False

            csv_recorder.stop_recording()


def data_received_callback(dmx_data):
    fps_calculator.chrono()

    if len(dmx_data) != 512:
        print(f"Unexpected data length encountered: {len(dmx_data)}")

        exit()

    dmx_data_to_record = []
    for index_to_extract in dmx_data_indices_to_record:
        dmx_data_to_record.append(dmx_data[index_to_extract])

    table = [
        ['Channel'] + dmx_channels_to_record,
        ['Value'] + dmx_data_to_record
    ]
    print(tabulate(table, headers='firstrow', tablefmt='simple_grid'))

    if is_recording:
        csv_recorder.record_frame(dmx_data_to_record)

    fps = fps_calculator.calculate_average_fps()

    print(f"{'(REC) ' if is_recording else ''}Received frame - FPS: {round(fps)}")


if __name__ == "__main__":
    try:
        with open("config.yaml", 'r') as stream:
            config = yaml.safe_load(stream)
    except yaml.YAMLError as exception:
        print("Error in config file:", exception)

    args = ArgumentsService.parse_arguments()

    csv_recorder = CsvRecorder(config)

    channel_range_parser = ChannelRangeParser()
    dmx_channels_to_record = channel_range_parser.parse(args.dmx_channels)
    dmx_data_indices_to_record = [dmx_channel - 1 for dmx_channel in dmx_channels_to_record]

    universe = args.artnet_universe
    artnet_server = StupidArtnetServer()

    recording_file_prefix = args.recording_file_prefix

    fps_calculator = FpsCalculator()
    fps_calculator.start()

    universe_listener = artnet_server.register_listener(
        universe,
        callback_function=data_received_callback
    )

    print(artnet_server)
    print('Waiting for ArtNet data...')

    listen_keyboard(
        on_press=on_keypress,
        until="esc",
    )

    print('You have pressed ESC, exiting the loop.')
