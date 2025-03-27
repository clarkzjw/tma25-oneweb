import re
import pytz
import numpy as np

from datetime import datetime
from dataclasses import dataclass

UT_ID = ""
FIXED_SIMULATION_DURATION = 0
RTT_DOWNSAMPLE_RATE = 1
SINR_DOWNSAMPLE_RATE = 1
LOAD_PREPROCESSED = True


@dataclass
class Latency:
    filename: str
    seq_ts: np.ndarray
    rtt: np.ndarray

    def len(self):
        assert len(self.seq_ts) == len(self.rtt)
        return len(self.seq_ts)

    def __init__(self, filename: str, seq_ts: list, rtt: list):
        self.filename = filename
        self.seq_ts = np.array(seq_ts)
        self.rtt = np.array(rtt)

        if RTT_DOWNSAMPLE_RATE > 1:
            self.seq_ts = self.seq_ts[::RTT_DOWNSAMPLE_RATE]
            self.rtt = self.rtt[::RTT_DOWNSAMPLE_RATE]

        assert len(self.seq_ts) == len(self.rtt)


def load_ping(filename: str):
    if filename.endswith(".txt"):
        with open(filename, "r") as f:
            seq_list = []
            rtt_list = []
            timestamp_list = []
            content = f.readlines()
            # tqdm.write(f"Loading {filename}")
            for line in content:
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
