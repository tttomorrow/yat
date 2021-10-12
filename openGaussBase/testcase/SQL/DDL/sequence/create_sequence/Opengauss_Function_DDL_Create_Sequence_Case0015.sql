--  @testpoint:两种方式调用nextval函数
--创建序列
drop SEQUENCE if exists serial_a;
CREATE SEQUENCE serial_a INCREMENT by 2 MAXVALUE 5 cycle;
--调用函数，从序列中选出下一个数字（1）
SELECT nextval('serial_a');
--调用函数，从序列中选出下一个数字（3）
select serial_a.nextval;
--删除序列
drop SEQUENCE serial_a;
