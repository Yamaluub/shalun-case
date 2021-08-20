#-------------- shalun-case --------------#
IEC61850 and whitelist example
### inverter gateway ###
1. sudo reboot         //重啟pi
2. ./close_iptables.sh //關閉防火牆
3. 開啟inverter (跑在 port:6688)
    cd /inverter_api/MobusClient/modbusController 
    sudo python service.py //取得變流器中，七段顯示器的值(為了遠端操作時能看變流器是否開關)。
