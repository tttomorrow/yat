-- @testpoint: 插入不符合设定范围值，合理报错
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS type_bit02;
CREATE TABLE type_bit02 (name bit(3));

--插入数据
--超出字段设定长度
insert into type_bit02 values (B'1011');
--不足字段设定长度
insert into type_bit02 values (B'10');

--插入失败，查看数据
select * from type_bit02;

--清理环境
drop table type_bit02;