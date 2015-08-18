1. 假设所有文件放在目录 DIR 下
2. 在使用前, 需要修改 profile.tin, 填上自己的 user 和 password

linux / cygwin
----------
cd DIR; 
tt++ profile.tin

对于 linux 和 cygwin, 通过 pkuxkx 脚本启动可以提供自动重新登录的功能,
用法:
1. 修改 pkuxkx 中的 pass 为登录密码
2. cd DIR; ./pkuxkx ID

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

修改门派信息, 可以参考 shaolin 这个文件. 

Requirements
----------
1. tintin++
2. sqlite3
3. python3
4. 可选: libnotify-bin, notifu (for cygwin), mplayer, sleekxmpp (for xmpp notification)
 
