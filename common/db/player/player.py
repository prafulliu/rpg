# -*- coding: utf-8 -*
#
# created by: liup Pengfei

import pymongo
import os
import time
import config.playerconfig as playerconfig
import csv

#connection = pymongo.Connection('localhost', 27017)
connection = pymongo.Connection()
db = connection.rpg
collection = db.player

class CPlayer():
    #创建角色
    def __init__(self, name, camp, occupation, zone, passport_id):
        self.passport_id      = passport_id
        self.occupation       = occupation
        self.create_time      = time.time() 
        self.last_login_time  = 0
        self.last_login_map   = 0
        self.zone             = 0
        self.cur_mapid        = 0
        self.x                = 0
        self.y                = 0
        self.name             = name

        #self.sex              = 0 
        #self.head_cg          = 0 
        #self.look             = 0 
        #以上三项可以通过查CSV表实现

        self.camp             = camp
        self.lv               = 1
        self.exp              = 0
        self.exp_max          = 0
        self.sp               = 0
        self.sp_max           = 0
        self.title            = []
        self.title_now        = 0
        self.silver_pack      = 0
        self.silver_warehouse = 0
        self.gold_pack        = 0
        self.gold_warehouse   = 0
        self.jade_pack        = 0
        self.jade_warehouse   = 0
        self.prepaid_score    = 0
        self.activity_score   = 0
        self.achieve_score    = 0
        self.guild_score      = 0

        collection.insert(vars(self))

def check_player(zone, passport_id, sitekey, sign):
    retVal = {}
    print zone
    print playerconfig.ZONE
    if zone in playerconfig.ZONE:
        player = collection.find_one({"passport_id":passport_id, "zone":zone})
        value = {}
        if player:
            value['player'] = player
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
        name_count = collection.find({'name':name}).count()
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
        passport_id_count = collection.find({'passport_id':passport_id}).count()
        if passport_id_count < playerconfig.MAX_PLAYER_CREATED:
            result = True
    return result

def creat_player(name, camp, occupation, zone, passport_id):
    #创建角色
    retVal = {}
    if check_name(name):
        if check_camp(camp):
            if check_occupation(occupation):
                if check_zone(zone):
                    if check_passport_id(passport_id):
                        p = CPlayer(name, camp, occupation, zone, passport_id)
                        retVal['value'] = vars(p)
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
    name          = 'lily'
    camp          = 1
    occupation    = 2
    zone          = 1
    passport_id   = '2'
    #p = CPlayer(passport, name, camp, occupation)
    #r = checkPlayer(0, '1', 0, 0)
    #print r

    #checkName('lily')
    
    r = creat_player(name, camp, occupation, zone, passport_id)
    print r
