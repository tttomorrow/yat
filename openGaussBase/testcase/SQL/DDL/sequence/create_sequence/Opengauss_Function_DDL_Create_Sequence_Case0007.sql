--  @testpoint:创建一个名为serial的递增序列，从101开始, CACHE参数测试
--cache20
drop SEQUENCE if exists serial_1;
CREATE SEQUENCE serial_1
 START 101
 CACHE 20;
 --从序列中选出下一个数字(101)
SELECT nextval('serial_1');
--查询序列信息（last_value为120，序列超过120，ast_value以等差20递增）
select sequence_name,last_value,start_value,cache_value from serial_1;
--cache -10，合理报错
drop SEQUENCE if exists serial_2;
CREATE SEQUENCE serial_2
 START 101
 CACHE -10;
--cache 0，合理报错
drop SEQUENCE if exists serial_3;
CREATE SEQUENCE serial_3
 START 101
 CACHE 0;
 --删除序列
 drop SEQUENCE serial_1;