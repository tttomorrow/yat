--  @testpoint:事务中，执行ALTER SEQUENCE MAXVALUE
--创建序列
drop SEQUENCE if exists serial_7;
CREATE SEQUENCE serial_7 INCREMENT by 2 MAXVALUE 5;
--开启事务
start transaction;
--修改序列最大值，合理报错
ALTER SEQUENCE serial_7 MAXVALUE 10;
--结束事务
 commit;
--删除序列
 drop SEQUENCE serial_7;