-- @testpoint: 插入设定长度边界值
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS type_bit05;
CREATE TABLE type_bit05 (name bit(3));

--插入数据
insert into type_bit05 values (B'101');
insert into type_bit05 values (B'111');

--插入成功，查看数据
select count(*) from type_bit05;

--清理环境
drop table type_bit05;