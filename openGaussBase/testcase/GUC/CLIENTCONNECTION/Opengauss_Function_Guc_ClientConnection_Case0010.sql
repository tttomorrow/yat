-- @testpoint: 设置参数search_path为不存在值，设置成功，建表，合理报错
--查看默认值
show search_path;
--设置为不存在的模式
drop schema if exists t_myschema010 cascade;
set search_path to t_myschema010;
--建表，报错
drop table if exists test_search_path010;
create table test_search_path010(id int);
--设置数字
set search_path to 110000;
--建表，报错
drop table if exists test_search_path010_bak;
create table test_search_path010_bak(id int);
--设置为特殊字符，报错
set search_path to *&$#^;
--恢复默认
set search_path to "$user",public;
show search_path;