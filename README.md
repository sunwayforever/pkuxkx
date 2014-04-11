1.  假设所有文件放在 *home/sunway*.tt 下

2.  执行以下命令来启动: tt++ *home/sunway*.tt/character/xxx.tin 其中 xxx.tin 对应着游戏角色的信息, 包含门派,用户名,密码等, 请自行编辑. 模板为:
    
        #var HOME /home/sunway
        #nop 这个 HOME 变量需要与文件所在路径一致
        #var XKX_PASSWORD password
        #var char_name 金贝贝;
        #var char_id bbkin;
        #read ${HOME}/.tt/main.tin;
        #read ${HOME}/.tt/plugin/spec/chaoting.tin;
        #session bbkin pkuxkx.net 8080; ${char_id}; ${XKX_PASSWORD};
