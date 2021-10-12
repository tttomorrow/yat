--  @testpoint:修改序列的归属列
--创建一个名为serial的递增序列，从101开始
drop SEQUENCE if exists a_serial;
CREATE SEQUENCE a_serial START 101;
--创建一个表,定义默认值
drop table if exists T1;
CREATE TABLE T1(C1 bigint default nextval('a_serial'));
--将序列a_serial的归属列变为T1.C1
ALTER SEQUENCE a_serial OWNED BY T1.C1;
--删除表
drop table  T1;
--查询序列，序列不存在，合理报错
select * from a_serial;

