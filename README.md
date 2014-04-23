1.  假设所有文件放在 /home/sunway/.tt 下

2.  执行以下命令来启动: tt++ xxx.tin 其中 xxx.tin 对应着游戏角色的登录
    信息和 HOME 变量, 模板为
    
        #var HOME /home/sunway
        #nop 这个 HOME 变量需要与文件所在路径一致
        #read ${HOME}/.tt/main.tin;
        #session bbkin pkuxkx.net 8080; bbkin; password;
