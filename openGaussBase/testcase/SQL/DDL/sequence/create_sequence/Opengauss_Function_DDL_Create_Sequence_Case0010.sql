--  @testpoint:创建序列，指定cycle
--创建序列，指定cycle
drop SEQUENCE if exists serial_7;
CREATE SEQUENCE serial_7 INCREMENT by 2 MAXVALUE 5 cycle;
--从序列中选出下一个数字(1)
SELECT nextval('serial_7');
--从序列中选出下一个数字(3)
SELECT nextval('serial_7');
--从序列中选出下一个数字(5)
SELECT nextval('serial_7');
--再次调用函数，返回1，达到最大值，继续循环
SELECT nextval('serial_7');
--删除序列
drop SEQUENCE serial_7;