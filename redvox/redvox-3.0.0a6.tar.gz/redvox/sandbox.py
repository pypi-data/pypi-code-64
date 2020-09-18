from datetime import datetime, timezone
from typing import List

import redvox.api1000.io_raw as io
from redvox.api1000.wrapped_redvox_packet.wrapped_packet import WrappedRedvoxPacketM


def main():
    read_filter = io.ReadFilter(start_dt=datetime(2020, 9, 14, 22),
                                end_dt=datetime(2020, 9, 14, 23),
                                station_ids={"1637110001", "1637610030"})

    read_result = io.read_structured("/home/opq/data/api_m/api1000", read_filter)

    for summary in read_result.get_station_summaries():
        print(summary)


if __name__ == "__main__":
    main()
