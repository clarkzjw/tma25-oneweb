# flake8: noqa: E501

import csv
import pytz
import numpy as np

from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from typing import Any


UT_ID = ""
FIXED_SIMULATION_DURATION = 0
RTT_DOWNSAMPLE_RATE = 1
SINR_DOWNSAMPLE_RATE = 1
LOAD_PREPROCESSED = True


class Error(BaseException):
    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> Any:
        return self.message


class CONSTELLATION(Enum):
    ONEWEB = "ONEWEB"


@dataclass
class AIM:
    constellation: CONSTELLATION
    filename: str
    handover_ts: np.ndarray
    sat_ids: np.ndarray
    seq_ts: np.ndarray
    avg_sinr: np.ndarray
    pointing_status: np.ndarray

    def len(self):
        assert len(self.handover_ts) == len(self.sat_ids)
        assert len(self.avg_sinr) == len(self.seq_ts)
        return len(self.seq_ts)

    def __init__(
        self,
        filename: str,
        handover_ts: list,
        seq_ts: list,
        sat_ids: list,
        avg_sinr: list,
        pointing_status: list,
    ):
        self.filename = filename
        self.handover_ts = np.array(handover_ts)
        self.seq_ts = np.array(seq_ts)
        self.sat_ids = np.array(sat_ids)
        self.avg_sinr = np.array(avg_sinr)
        self.pointing_status = np.array(pointing_status)


def process_aim_file(filepath: str) -> AIM:
    handover_ts = []
    seq_ts = []
    sat_ids = []
    avg_sinr = []
    pointing_status = []
    last_satellite_id = -1

    with open(filepath, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            # 2024-11-29T22:53:19.049Z,-1.96,66256929,33,HL1120W,0,0,HCS,APT,118.865,50.771,50.599,44.549,14362000000,11325000000,-178.850,-0.269,-9.636,{"INTEGRATOR_PARAMS":{"CALIBRATION_STATUS":"Complete","MAX_SINR":-1.70,"POINTING_SCORE":96.4,"POINTING_STATE":"Pointing"}}

            if row[1] != "":
                seq_ts.append(
                    datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                        tzinfo=pytz.utc
                    )
                )
                avg_sinr.append(float(row[1]))
            else:
                continue

            if len(row) > 4 and "Pointing" in row[21]:
                pointing_status.append(1)
            else:
                pointing_status.append(0)

            if row[3] != last_satellite_id:
                last_satellite_id = row[3]
                handover_ts.append(seq_ts[-1])
                sat_ids.append(last_satellite_id)

    if len(sat_ids) != len(handover_ts):
        raise Error(f"Length of sat_ids and handover_ts do not match: {filepath}")

    if len(seq_ts) != len(avg_sinr):
        raise Error(f"Length of seq_ts and avg_sinr do not match: {filepath}")

    if SINR_DOWNSAMPLE_RATE > 1:
        seq_ts = seq_ts[::SINR_DOWNSAMPLE_RATE]
        avg_sinr = avg_sinr[::SINR_DOWNSAMPLE_RATE]

    return AIM(filepath, handover_ts, seq_ts, sat_ids, avg_sinr, pointing_status)
