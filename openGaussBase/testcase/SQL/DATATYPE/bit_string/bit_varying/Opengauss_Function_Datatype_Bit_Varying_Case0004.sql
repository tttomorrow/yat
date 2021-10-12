-- @testpoint: 插入空值
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS type_bit_varying04;
CREATE TABLE type_bit_varying04 (name bit varying(3));

--插入数据
insert into type_bit_varying04 values (B'');
insert into type_bit_varying04 values (null);

--插入失败，查看数据
select * from type_bit_varying04;

--清理环境
drop table type_bit_varying04;
