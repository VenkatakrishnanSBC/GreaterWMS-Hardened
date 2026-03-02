"""
FEATURE-005: Label printing module for GreaterWMS.

Generates ZPL (Zebra Programming Language) and ESC/POS commands
for thermal label printers. Supports:
- Barcode labels for goods
- Bin location labels
- Shipping labels
- Pick list labels
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ZPLLabel:
    """
    ZPL label generator for Zebra thermal printers.

    Builds ZPL commands for common warehouse label types.
    Output can be sent to a Zebra printer via raw socket (port 9100)
    or through a print server.
    """

    def __init__(self, width_mm: int = 100, height_mm: int = 50, dpi: int = 203):
        self.width = width_mm
        self.height = height_mm
        self.dpi = dpi
        self._commands: list = []
        self._start()

    def _start(self) -> None:
        """Initialize ZPL label."""
        self._commands = ['^XA']  # Start format
        self._commands.append(f'^PW{int(self.width * self.dpi / 25.4)}')
        self._commands.append(f'^LL{int(self.height * self.dpi / 25.4)}')

    def add_text(self, x: int, y: int, text: str, font_size: int = 30) -> 'ZPLLabel':
        """Add text to the label."""
        self._commands.append(f'^FO{x},{y}')
        self._commands.append(f'^A0N,{font_size},{font_size}')
        self._commands.append(f'^FD{text}^FS')
        return self

    def add_barcode_128(self, x: int, y: int, data: str, height: int = 80) -> 'ZPLLabel':
        """Add Code 128 barcode."""
        self._commands.append(f'^FO{x},{y}')
        self._commands.append(f'^BCN,{height},Y,N,N')
        self._commands.append(f'^FD{data}^FS')
        return self

    def add_qr_code(self, x: int, y: int, data: str, size: int = 4) -> 'ZPLLabel':
        """Add QR code."""
        self._commands.append(f'^FO{x},{y}')
        self._commands.append(f'^BQN,2,{size}')
        self._commands.append(f'^FDLA,{data}^FS')
        return self

    def add_line(self, x: int, y: int, width: int, thickness: int = 2) -> 'ZPLLabel':
        """Add horizontal line."""
        self._commands.append(f'^FO{x},{y}^GB{width},{thickness},{thickness}^FS')
        return self

    def build(self) -> str:
        """Generate the complete ZPL string."""
        self._commands.append('^XZ')  # End format
        return '\n'.join(self._commands)

    def print_to_network(self, printer_ip: str, port: int = 9100) -> bool:
        """Send label to a network-connected Zebra printer."""
        import socket
        try:
            zpl = self.build()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((printer_ip, port))
                s.sendall(zpl.encode('utf-8'))
            logger.info(f"Label sent to {printer_ip}:{port}")
            return True
        except Exception as e:
            logger.error(f"Print failed to {printer_ip}:{port}: {e}")
            return False


def goods_label(
    goods_code: str,
    goods_desc: str,
    bar_code: str,
    supplier: str = '',
) -> str:
    """
    Generate a goods barcode label.

    Args:
        goods_code: The goods code.
        goods_desc: Description text.
        bar_code: Barcode data.
        supplier: Optional supplier name.

    Returns:
        ZPL string ready to send to printer.
    """
    label = ZPLLabel(width_mm=100, height_mm=60)
    label.add_text(30, 20, goods_code, font_size=40)
    label.add_text(30, 70, goods_desc[:30], font_size=25)
    if supplier:
        label.add_text(30, 100, f"Supplier: {supplier}", font_size=20)
    label.add_line(30, 130, 700)
    label.add_barcode_128(30, 150, bar_code, height=80)
    return label.build()


def bin_label(bin_name: str, bin_property: str, bin_size: str) -> str:
    """Generate a bin location label with QR code."""
    label = ZPLLabel(width_mm=80, height_mm=50)
    label.add_text(30, 20, bin_name, font_size=50)
    label.add_text(30, 80, f"{bin_property} | {bin_size}", font_size=25)
    label.add_qr_code(400, 20, bin_name, size=5)
    return label.build()


def shipping_label(
    dn_code: str,
    from_name: str,
    to_name: str,
    to_address: str,
    tracking_number: str = '',
) -> str:
    """Generate a shipping label for outbound delivery."""
    label = ZPLLabel(width_mm=100, height_mm=150)
    label.add_text(30, 20, "SHIP TO:", font_size=25)
    label.add_text(30, 55, to_name, font_size=35)
    label.add_text(30, 100, to_address[:40], font_size=25)
    label.add_line(30, 140, 700)
    label.add_text(30, 160, f"FROM: {from_name}", font_size=20)
    label.add_text(30, 190, f"DN: {dn_code}", font_size=25)
    label.add_line(30, 230, 700)
    if tracking_number:
        label.add_barcode_128(30, 250, tracking_number, height=100)
    return label.build()
