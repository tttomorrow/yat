-- @testpoint: 插入中文字符


drop table if exists name_08;
CREATE TABLE name_08 (id name);
insert into name_08 values ('我是测试数据我是测试数据我是测试数据我是测试数据');
select * from name_08;
drop table name_08;