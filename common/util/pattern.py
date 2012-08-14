# -*- coding: utf-8 -*-

def to_hex(val):
	if val and (val >=0 and val <= 0x99999999):
		val = hex(val)
		val_hex = val[2:]
		while (len(val_hex) < 8):
			val_hex = '0'+val_hex
		val_hex = '0x'+val_hex
		return val_hex
	else:
		return


if __name__ == "__main__":
	print to_hex(-1)
