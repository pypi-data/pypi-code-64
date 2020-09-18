from typing import List

import redvox.api1000.io_raw as io
from redvox.api1000.wrapped_redvox_packet.wrapped_packet import WrappedRedvoxPacketM


def main():
    # Read all API M files in a given directory
    unstructured_base_dir: str = "/home/opq/data/api_m/unstructured"
    read_result: io.ReadResult = io.read_unstructured(unstructured_base_dir)

    for summary in read_result.get_station_summaries():
        print(summary)

    # Let's go ahead and access the packets for station 1637610001
    # The packets can either be accessed by the station id or a combination of the station_id:station_uuid.

    packets: List[WrappedRedvoxPacketM] = read_result.get_packets_for_station_id("1637610001")
    print(len(packets))


if __name__ == "__main__":
    main()
