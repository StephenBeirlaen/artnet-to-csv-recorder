class ChannelRangeParser:
    def parse(self, channel_range_input: str):
        channels = sum(
            (
                (
                    list(
                        range(
                            *[
                                int(b) + c
                                for c, b in enumerate(a.split('-'))
                            ]
                        )
                    )
                    if '-' in a else [int(a)]) for a in channel_range_input.split(',')
            ),
            []
        )

        # Remove duplicate values
        channels = list(set(channels))

        # Sort
        channels.sort()

        return channels
