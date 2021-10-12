--  @testpoint:使用drop同时删除多个序列名
--创建两个序列
drop SEQUENCE if exists t_serial2;
CREATE SEQUENCE t_serial2 START 101;
drop SEQUENCE if exists t_serial3;
CREATE SEQUENCE t_serial3 START 101;
--使用drop语句同时删除两个序列
drop SEQUENCE t_serial2,t_serial3;
