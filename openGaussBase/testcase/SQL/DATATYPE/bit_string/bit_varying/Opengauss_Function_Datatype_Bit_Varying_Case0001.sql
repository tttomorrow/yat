-- @testpoint: 插入正常值
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS type_bit_varying01;
CREATE TABLE type_bit_varying01 (name bit varying);

--插入数据
insert into type_bit_varying01 values (B'1');

--插入成功，查看数据
select * from type_bit_varying01;

--清理数据
drop table type_bit_varying01;