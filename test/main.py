from log.log import LOG, TYPE



LOG.setLevel(TYPE.INFO)
LOG.info("this is a log")

s = 'id, name, type, chapter, composite, subtasks, daily_level, camp,\
occupation, min_prestige, sns, can_giveup, can_help, can_loop, max_loop,\
time_limit, accept_itemid, snpc, enpc, stalk, etalk, pcon, pack, task_accept,\
task_down, task_reward, pre_tid, next_tid, min_lv, max_lv, kill_cdt, item_cdt,\
use_item, r_exp, r_silver, r_gold, r_jade, r_prestige, r_item, r_master,\
r_conjugal, r_integral, r_point, can_entrust, entrust_token, entrust_silver,\
entrust_gold, entrust_time'

while len(s)>0:
	word = s[0:s.index(',')]
	print word
	break
