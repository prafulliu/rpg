import inspect

def check_pkt_data_integrity(func, pkt):
	lack_key_list = []
	result = True
	ret = inspect.getargspec(func)
	for arg in ret.args:
		if not pkt.has_key(arg):
			lack_key_list.append(arg)
			result = False
	return result, lack_key_list
