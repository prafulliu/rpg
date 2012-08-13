简单解释下服务器内部框架， 我们游戏会有一个gate server python的进程， 首先以client身份去连接gate server, 
刚连接上时， 先发送以下东西过去验证：
[uint32 channel_id][string channel_name][string key]
这样向gate server注册 自己的频道ID, 频道名称。 key为校验用的
（上面[ ] 只是表示分隔， 在协议包里没这字符的）
而其中string类型又是这样表示的： [length][content]
即先发一个uint32类型的整数表示字符串的长度， 然后接着才是字符串的内容。
gate server收到后， 如果验证不成功， 就直接close掉连接。 如果验证成功，
则接下来gate server就会将从flash as3端接收到的包转发到对应的python进程去处理


gate server和python进程之间连接且验证注册服务成功以后， 之间通讯的包的格式是：
gate server 发给python进程的：
[uint32_t player_id][uint16_t msg_channel][uint16_t cmd][string amf3_data]

返回给gate server的：

有点修改：
返回给gate server的：
[uint8_t flag][uint32_t targetLen][target_players][uint8_t ch='\0'][uint16_t
																	msg_channel][uint16_t
							  cmd][string amf3_data]
targetLen指示[target_players]的字节长度加上'\0'分隔字符长度。所以targetLen长度最小为1

flag=0, 返回给单个或多个指定玩家， 此时target_players内容为  [uint32_t
																				count][uint32_t
						   player_id1]...[uint32_t player_idN]
flag=1, 广播给所有玩家， 此时没有target_players项
flag=2等其他， 预留
 
===================================================================

update:
gate server 发给python进程的请求：
[uint32_t client_id][uint16_t msg_channel][uint16_t cmd][string amf3_data]
对于玩家角色未完成登录的情况，
client_id的含义为session_id（此时python进程需要记住它，并在应答中按原数值返回，但无需存储它），
对于玩家角色已完成登录的情况，client_id的含义为角色的player_id本身
返回给gate server的：
[uint8_t flag][uint32_t targetLen][target_players][uint8_t ch='\0'][uint16_t
																	msg_channel][uint16_t
							  cmd][string amf3_data]
targetLen指示[target_players]的字节长度加上'\0'分隔字符长度。所以targetLen长度最小为1
对玩家角色未登录的情况， target_players是只有上面的请求中的client_id一项

