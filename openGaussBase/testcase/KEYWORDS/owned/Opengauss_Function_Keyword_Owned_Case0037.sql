--  @testpoint:opengauss关键字owned(非保留)，修改序列归属列

--创建一个名为serial的递增序列，从101开始。
CREATE SEQUENCE serial_1 START 101;

--创建一个表,定义默认值。
CREATE TABLE T1(C1 bigint default nextval('serial_1'));

--将序列serial的归属列变为T1.C1。
ALTER SEQUENCE serial_1 OWNED BY T1.C1;

--删除序列
DROP SEQUENCE serial_1 cascade;
DROP TABLE T1;


