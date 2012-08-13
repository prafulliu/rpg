# -*- coding: utf-8 -*
#
# created by: liup Pengfei
import os
import time
import config.playerconfig as playerconfig
import db.base.mongoconf as mongoconf
import config.mapconfig as mapconfig
from db.base.databaseaccess import CDataBaseAccess
from db.base.autoincpk import CAutoIncPk

rpg_access = CDataBaseAccess(mongoconf.IP, mongoconf.PORT,
							mongoconf.DB_RPG)
COL_PLAYER = mongoconf.COL_PLAYER

class CPlayer():
    #创建角色
    def __init__(self, name, camp, occupation, zone, passport_id):
		_id = CAutoIncPk().get_pk_by_name(COL_PLAYER)
		self._id                     = _id
		self.passport_id             = passport_id
		self.occupation              = occupation
		self.create_time             = time.time()
		self.last_login_time         = 0
		self.last_login_map          = 0
		self.zone                    = 0
		self.mapid                   = mapconfig.INIT_MAPID
		self.x                       = mapconfig.X
		self.y                       = mapconfig.Y
		self.dir                     = mapconfig.DOWN
		self.name                    = name

		self.camp                    = camp
		self.lv                      = 1
		self.exp                     = 0
		self.exp_max                 = 0
		self.sp                      = 0
		self.sp_max                  = 0
		self.title                   = []
		self.title_now               = 0
		self.silver_pack             = 0
		self.silver_warehouse        = 0
		self.gold_pack               = 0
		self.gold_warehouse          = 0
		self.jade_pack               = 0
		self.jade_warehouse          = 0
		self.prepaid_score           = 0
		self.activity_score          = 0
		self.achieve_score           = 0
		self.guild_score             = 0
        
        
		self.str                     = 0
		self.str_potential           = 0
		self.str_add                 = 0
		self.str_max                 = 0

		self.int                     = 0
		self.int_potential           = 0
		self.int_add                 = 0
		self.int_max                 = 0

		self.phy                     = 0
		self.phy_potential           = 0
		self.phy_add                 = 0
		self.phy_max                 = 0

		self.agi                     = 0
		self.agi_potential           = 0
		self.agi_add                 = 0
		self.agi_max                 = 0

		self.potential               = 0

		self.physical_dmg            = 0
		self.magic_dmg               = 0
		self.physical_def            = 0
		self.magic_def               = 0

		self.hp                      = playerconfig.INIT_HP
		self.hp_max                  = playerconfig.INIT_HP 
		self.mp                      = playerconfig.INIT_MP
		self.mp_max                  = playerconfig.INIT_MP
		self.acc                     = 0
		self.miss                    = 0
		self.cri                     = 0
		self.tenacity                = 0
		self.slowdown_def            = 0
		self.vertigo_def             = 0
		self.freeze_def              = 0
		self.att_speed               = 0
		self.move_speed              = 0
		self.warfare                 = 0
		self.sunder_armor            = 0
		self.super_armor             = 0
		self.rigidity                = 0
		self.rig_def                 = 0
		self.energy                  = 0

		rpg_access.insert(COL_PLAYER, vars(self))

def check_player(zone, passport_id, sitekey, sign):
    retVal = {}
    if zone in playerconfig.ZONE:
        player = rpg_access.query_one(COL_PLAYER, {"passport_id":passport_id, "zone":zone})
        value = {}
        if player:
            player_info = get_player_info(player)
            value['player'] = player_info
            value['create'] = True
        else:
            value['create'] = False
        
        result = 0
        retVal['value'] = value
    else:
        result = 1
    
    retVal['result'] = result 
    return retVal

def get_recomand_camp():
    #获取推荐阵营
    camp = 1
    return camp

def get_recomand_occupation():
    #获取推荐职业
    occupation = 1
    return occupation

def get_recommand_player_info():
    #获取推荐角色信息
    retVal = {}
    retVal['result'] = 0
    value = {}
    value['camp'] = get_recomand_camp()
    value['occupation'] = get_recomand_occupation()
    retVal['value'] = value
    return retVal
        
def check_name(name):
	#检查用户名(name)
	result = True
	if name != None:
		name_count = rpg_access.query(COL_PLAYER, {'name':name}).count()
		if name_count != 0:
			result = False
	return result

def check_camp(camp):
    #检查阵营(camp)
    result = False
    if camp in playerconfig.CAMP:
        result = True
    return result

def check_occupation(occupation):
    #检查职业(occupation)
    result = False
    if occupation in playerconfig.OCCUPATION:
        result = True
    return result

def check_zone(zone):
    #检查服务器(zone)
    result = False
    if zone in playerconfig.ZONE:
        result = True
    return result

def check_passport_id(passport_id):
    #检查账号名称(passport_id)
    result = False
    if passport_id != None:
        passport_id_count = rpg_access.query(COL_PLAYER, {'passport_id':passport_id}).count()
        if passport_id_count < playerconfig.MAX_PLAYER_CREATED:
            result = True
    return result

def get_map_name(mapid):
    map_name = mapconfig.INIT_MAPNAME
    return map_name 

def get_player_look(playerid):
    look = []
    return look

def get_title_name(titleid):
    title_name = ''
    return title_name

def get_player_info(player):
    player_info = {}
    if player:
        player_info['playerid']   = player['_id']
        player_info['mapid']      = player['mapid']
        map_name = get_map_name(player['mapid'])
        player_info['map_name']   = map_name 
        player_info['x']          = player['x']
        player_info['y']          = player['y']
        player_info['dir']        = player['dir']
        player_info['name']       = player['name']
        player_info['look']       = get_player_look(player['_id'])
        player_info['occupation'] = player['occupation']
        player_info['title_now']  = get_title_name(player['title_now'])
        player_info['hp']         = player['hp']
        player_info['hp_max']     = player['hp_max']
        player_info['mp']         = player['mp']
        player_info['mp_max']     = player['mp_max']
        player_info['lv']         = player['lv']
    return player_info

def creat_player(name, camp, occupation, zone, passport_id):
    #创建角色
    retVal = {}
    if check_name(name):
        if check_camp(camp):
            if check_occupation(occupation):
                if check_zone(zone):
                    if check_passport_id(passport_id):
                        p = CPlayer(name, camp, occupation, zone, passport_id)
                        player_info = get_player_info(vars(p))
                        value = {}
                        value['player'] = player_info
                        retVal['value'] = value
                        result = 0 
                    else:
                        result = 5
                else:
                    result = 4
            else:
                result = 3
        else:
            result = 2
    else:
        result = 1
    retVal['result'] = result
    return retVal

if __name__ == "__main__":
    name          = '哈哈'
    print 'type name:', type(name)
    camp          = 1
    occupation    = 2
    zone          = 0
    passport_id   = '1'
    sitekey       = 0
    sign          = 0   
    #p = CPlayer(passport, name, camp, occupation)
    #r = checkPlayer(0, '1', 0, 0)
    #print r

    #checkName('lily')
    
    r = creat_player(name, camp, occupation, zone, passport_id)
    #r = check_player(zone, passport_id, sitekey, sign)
    #print r['value']['player']['name']
    print r
    #data = {'name':'草'}
    #print data
    #rpg_access.insert(COL_PLAYER, data)
    
