--  @testpoint:同时定义cache和maxvalue以及minvalue
--创建序列
--cache10,会有notice提示
drop SEQUENCE if exists serial_3;
CREATE SEQUENCE serial_3 INCREMENT by 2 MINVALUE 100 MAXVALUE 121 START 100 CACHE 10;
--查询序列信息
select sequence_name,last_value,start_value,cache_value,increment_by,max_value,min_value from serial_3 where sequence_name = 'serial_3';
--删除序列
drop SEQUENCE serial_3;