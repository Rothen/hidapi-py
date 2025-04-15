from .out_report import OutReport
from .enums import OutReportLength


class Bt01OutReport(OutReport):
    def to_bytes(self) -> bytes:
        out_report_bytes: bytes = bytearray(OutReportLength.BT_31)
        return out_report_bytes
