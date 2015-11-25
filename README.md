假设所有文件放在目录 DIR 下

linux / cygwin
----------
cd DIR; ./pkuxkx ID 'PASSWORD'

添加新的门派支持
----------
脚本会检测门派, 所有门派信息放在 plugin/spec 目录, 不同门派需要设
置的信息包括:

1. 战斗相关
2. 领悟地点相关
3. 门忠 NPC 相关
4. 传授技能的 NPC 相关

修改门派信息, 可以参考 shaolin 这个文件. 

Requirements
----------
1. tintin++
2. sqlite3
3. python3
4. Optional: sleekxmpp (for xmpp notification)
