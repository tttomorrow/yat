--  @testpoint:创建序列，CYCLE测试（使序列达到maxvalue或者minvalue后可循环并继续下去）
--testpoint1:创建序列，指定maxvalue
drop SEQUENCE if exists serial_3;
CREATE SEQUENCE serial_3 INCREMENT by 2 MAXVALUE 5;
--从序列中选出下一个数字(1)
SELECT nextval('serial_3');
--从序列中选出下一个数字(3)
SELECT nextval('serial_3');
--从序列中选出下一个数字(5)
SELECT nextval('serial_3');
--从序列中选出下一个数字，合理报错，序列达到其最大值后任何对nextval的调用都会返回一个错误。默认是NO CYCLE
SELECT nextval('serial_3');
--删除序列
drop SEQUENCE serial_3;
--testpoint2:创建序列，指定maxvalue时添加NO CYCLE
drop SEQUENCE if exists serial_4;
CREATE SEQUENCE serial_4 INCREMENT by 2 MAXVALUE 5 NO CYCLE;
--从序列中选出下一个数字(1)
SELECT nextval('serial_4');
--从序列中选出下一个数字(3)
SELECT nextval('serial_4');
--从序列中选出下一个数字(5)
SELECT nextval('serial_4');
--从序列中选出下一个数字，合理报错，序列达到其最大值后任何对nextval的调用都会返回一个错误。
SELECT nextval('serial_4');
--删除序列
drop SEQUENCE serial_4;
----testpoint3:创建序列，指定maxvalue时添加NOCYCLE
drop SEQUENCE if exists serial_5;
CREATE SEQUENCE serial_5 INCREMENT by 2 MAXVALUE 5 NOCYCLE;
--从序列中选出下一个数字(1)
SELECT nextval('serial_5');
--从序列中选出下一个数字(3)
SELECT nextval('serial_5');
--从序列中选出下一个数字(5)
SELECT nextval('serial_5');
--从序列中选出下一个数字，合理报错，序列达到其最大值后任何对nextval的调用都会返回一个错误。
SELECT nextval('serial_5');
--删除序列
drop SEQUENCE serial_5;