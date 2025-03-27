import re
import pytz

from datetime import datetime


def load_ping(filename: str):
    if filename.endswith(".txt"):
        with open(filename, "r") as f:
            seq_list = []
            rtt_list = []
            timestamp_list = []
            for line in f.readlines():
                match = re.search(
                    r"\[(\d+\.\d+)\].*icmp_seq=(\d+).*time=(\d+(\.\d+)?)", line
                )
                if match:
                    timestamp = datetime.fromtimestamp(
                        float(match.group(1)),
                        tz=pytz.utc,
                    )

                    seq = int(match.group(2))
                    rtt = float(match.group(3))
                    timestamp_list.append(timestamp)
                    seq_list.append(seq)
                    rtt_list.append(rtt)

    return timestamp_list, rtt_list
