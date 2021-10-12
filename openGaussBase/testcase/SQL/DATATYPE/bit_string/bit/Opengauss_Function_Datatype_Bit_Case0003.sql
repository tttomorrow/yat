-- @testpoint: 插入错误值，合理报错
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS type_bit03;
CREATE TABLE type_bit03 (name bit(3));

--插入数据
insert into type_bit03 values (B'201');

--插入失败，查看数据
select * from type_bit03;

--清理环境
drop table type_bit03;