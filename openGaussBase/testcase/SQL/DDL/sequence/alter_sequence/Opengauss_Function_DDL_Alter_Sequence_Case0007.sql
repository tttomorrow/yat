--  @testpoint:分别调用nextval、setval、currval函数,执行ALTER SEQUENCE语句
--创建序列
drop SEQUENCE if exists serial_d;
CREATE SEQUENCE serial_d INCREMENT by 2 MAXVALUE 15 cache 5;
--调用nextval(1)
select nextval('serial_d');
--执行alter语句
alter SEQUENCE serial_d MAXVALUE 21;
--调用nextval(11)
select nextval('serial_d');
--删除序列
drop SEQUENCE serial_d;
--创建序列
drop SEQUENCE if exists serial_e;
CREATE SEQUENCE serial_e INCREMENT by 2 MAXVALUE 15 cache 5;
--设置序列当前数值为11
select setval('serial_e',11);
--执行alter语句
alter SEQUENCE serial_e MAXVALUE 21;
select setval('serial_e',13);
--返回当前会话里最近一次nextval返回的指定的sequence的数值（13）
select currval('serial_e');
--删除序列
drop SEQUENCE serial_e;
