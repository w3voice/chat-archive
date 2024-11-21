import crc16
import base64

class InvalidAddress(Exception):
    pass

class Address:
    def __init__(self, b64=None):
        if b64 is None:
            self.b64 = None
            self.wc = None
            self.hash = None
        else:
            self.init_from_b64(b64)

    def init_from_b64(self, addr):
        self.wc, self.hash = base64_to_hex_addr(addr)
        self.b64 = addr

def base64_to_hex_addr(addr):
    try:
        addr = addr.replace('-', '+')
        addr = addr.replace('_', '/')
        addr = addr.encode()
        b = base64.b64decode(addr)
        crc = crc16.crc16xmodem(b[:34])
        if len(b) != 36:
            raise InvalidAddress("base64_to_hex_addr error: invalid length")
        if b[34] != (crc >> 8) or b[35] != (crc & 0xff):
        	raise InvalidAddress("base64_to_hex_addr error: invalid crc")
        workchain = int(b[1])
        if workchain >= 128:
        	workchain -= 256
        addr_hex = b[2:34].hex()
        return (workchain, int(addr_hex, 16))
    except InvalidAddress:
        raise
    except:
        raise InvalidAddress("base64_to_hex_addr error")
