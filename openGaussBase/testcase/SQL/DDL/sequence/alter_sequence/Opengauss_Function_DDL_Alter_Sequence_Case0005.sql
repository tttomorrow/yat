-- @testpoint: 修改序列其他参数（START，MINVALUE ）合理报错
--testpoint1:
drop SEQUENCE if exists serial;
CREATE SEQUENCE serial START 101;
--修改序列start,合理报错
alter SEQUENCE if exists serial START 100;
--删除序列
drop SEQUENCE serial;
--testpoint2:创建序列
drop SEQUENCE if exists serial2;
CREATE SEQUENCE serial2 MINVALUE 100 START 101;
--修改序列最小值，合理报错
alter SEQUENCE if exists serial2 MINVALUE 99;
--删除序列
drop SEQUENCE serial2;