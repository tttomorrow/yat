-- @testpoint: 将pg_catalog模式加入search_path设为搜素路径最后位置，有告警；建表，合理报错
--step1:查看默认搜索路径;expect:成功
show search_path;
--step2:设置搜索路径，系统路径在后;expect:成功
set search_path to "$user",publi,pg_catalog;
--step3:查看;expect:设置成功
show search_path;
--step4:创建表;expect:合理报错
drop table if exists t_clientconnection_0015;
create table t_clientconnection_0015(id int);
--step5:恢复默认;expect:成功
set search_path to "$user",public;
show search_path;