# shalun-case #
IEC61850 and whitelist example
### inverter gateway ###
1. sudo reboot         //重啟pi
2. ./close_iptables.sh //關閉防火牆
3. 開啟inverter (跑在 port:6688)
    cd /inverter_api/MobusClient/modbusController 
    sudo python service.py //取得變流器中，七段顯示器的值(為了遠端操作時能看變流器是否開關)。
### server ###
1. sudo reboot         //重啟pi
2. ./close_iptables.sh //關閉防火牆 
---------------------------------------
3. 打開iec61850通訊連線環境(用docker build, 昀陞已寫好.sh腳本,可vim run_61850_server.sh查看腳本內容)
    cd libiec61850/
    docker image ls
    sudo ./run_61850_server.sh no_tls latest 8102
    sudo ./run_61850_server.sh tls latest 8103 (這可以不用執行，因昀陞已經有設定(restart=always)成重開後會自動restart)
4. sudo getenforce //確認白名單狀態(是否啟動)
----------------------------------------
p.s: config_file 檔: 控制inverter開關與其他相關狀態的設定檔(若之後inverter gateway ip:port, name換了(因為router換了之類的)，要記得改)。
1.API 控制 inverter gateway的開關
2.取得inverter gateway的狀態
3.取得inverter gateway的資訊

### client ###
1. sudo reboot         //重啟pi
2. ./close_iptables.sh //關閉防火牆
---------------------------------------
3. 打開iec61850通訊連線環境(用docker build, 昀陞已寫好.sh腳本,可vim run_61850_server.sh查看腳本內容)
    cd libiec61850/
    docker image ls
    sudo ./run_61850_server.sh no_tls latest 8102
    sudo ./run_61850_server.sh tls latest 8103 (這可以不用執行，因昀陞已經有設定(restart=always)成重開後會自動restart)
4. ./inverter_info.sh no_tls 192.168.1.121 8102 //發訊息給server，透過server的config_file去跟inverter gateway取得inverter資訊
5. ./inverter_set.sh no_tls 192.168.1.121 inverter_off 8102 //發訊息給server，透過server的config_file去跟inverter gateway關閉變流器
6. ./inverter_set.sh no_tls 192.168.1.121 inverter_on 8102 //發訊息給server，透過server的config_file去跟inverter gateway啟動變流器
---------------------------------------
7. sudo getenforce //確認白名單狀態(是否啟動)
8. sudo setenforce 1 //開啟白名單防護(重開機時會關閉)，若要永久打開則需進到 sudo vim /etc/selinux/config 裡面改。
9. sudo setenforce 0 //關閉白名單防護。
9. whitelist_add.sh ~/libiec61850/inverter_set.sh //在白名單開啟的情況下，把想允許執行的shellscript加到白名單中。
10. whitelist_remove.sh ~/libiec61850/inverter_set.sh //在白名單開啟的情況下，把想移除執行的shellscript加到白名單中。
11. check_script.sh ~/libiec61850/inverter_set.sh //檢查想允許執行的shellscript是否被放在白名單裡
