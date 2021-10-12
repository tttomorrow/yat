-- @testpoint: 插入正常值
-- @modify at: 2020-11-04

--创建表
DROP TABLE IF EXISTS type_bit01;
CREATE TABLE type_bit01 (name bit);

--插入数据
insert into type_bit01 values (B'1');
insert into type_bit01 values (cast('001001' as bit));

--插入成功，查看数据
select * from type_bit01;

--清理环境
drop table type_bit01;