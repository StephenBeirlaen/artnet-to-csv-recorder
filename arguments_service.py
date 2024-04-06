import argparse


class ArgumentsService:
    @staticmethod
    def parse_arguments() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="ArtNet recorder")

        parser.add_argument(
            '--artnet-universe',
            type=int,
            default=0
        )

        parser.add_argument(
            '--dmx-channels',
            type=str,
            default=''
        )

        parser.add_argument(
            '--recording-file-prefix',
            type=str,
            default=''
        )

        args = parser.parse_args()

        return args
