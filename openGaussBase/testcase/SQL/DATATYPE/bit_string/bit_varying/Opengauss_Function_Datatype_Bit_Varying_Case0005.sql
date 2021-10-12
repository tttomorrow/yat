-- @testpoint: 插入边界值
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS type_bit_varying05;
CREATE TABLE type_bit_varying05 (name bit varying(3));

--插入数据
insert into type_bit_varying05 values (B'101');

--插入成功，查看数据
select * from type_bit_varying05;

--清理环境
drop table type_bit_varying05;