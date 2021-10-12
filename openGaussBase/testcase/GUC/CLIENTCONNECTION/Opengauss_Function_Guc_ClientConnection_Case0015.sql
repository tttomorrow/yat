-- @testpoint: 将pg_catalog模式加入search_path设为搜素路径最后位置，有告警；建表，合理报错
--查看
show search_path;
--设置
set search_path to "$user",publi,pg_catalog;
--查看
show search_path;
--创建表，报错
drop table if exists test_search_path015;
create table test_search_path015(id int);
--恢复默认
set search_path to "$user",public;
show search_path;