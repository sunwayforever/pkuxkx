1. 假设所有文件放在目录 DIR 下
2. 在使用前, 需要修改 profile.tin, 填上自己的 user 和 password

linux
----------
cd DIR; 
tt++ profile.tin

windows
----------
双击 DIR/wintin++/pkuxkx.bat

添加新的门派支持
----------
脚本会检测门派, 所有门派信息放在 plugin/spec 目录, 不同门派需要设
置的信息包括:

1. 战斗相关
2. 领悟地点相关
3. 门忠 NPC 相关
4. 传授技能的 NPC 相关

修改门派信息, 可以参考 gumu 这个文件. 另外, 因为领悟机器人使用 map 来走
路,所以还需要在 map 目录下自己建立一个相应的 map

