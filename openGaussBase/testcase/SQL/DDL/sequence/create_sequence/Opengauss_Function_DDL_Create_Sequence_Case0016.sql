--  @testpoint:事务中，调用nextval函数
--创建序列
drop SEQUENCE if exists serial_b;
CREATE SEQUENCE serial_b INCREMENT by 2 MAXVALUE 5 cycle;
--开启事务
start transaction;
--调用函数，从序列中选出下一个数字（1）
SELECT nextval('serial_b');
--结束事务
commit;
--调用函数，从序列中选出下一个数字（3）
select serial_b.nextval;
--再次开启事务，从序列中选出下一个数字（5）
start transaction;
select serial_b.nextval;
--回滚
rollback;
--从序列中选出下一个数字（1）,nextval操作不会回滚
select serial_b.nextval;
--删除序列
drop SEQUENCE serial_b;