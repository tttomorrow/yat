-- @testpoint: 查看max_identifier_length,创建表，表名长度超过63个字符，自动截取

--通过show方式查看
show max_identifier_length;

--创建表
drop table if exists max_length_table_123456789123456789123456789123456789123456789123456789;
create table max_length_table_123456789123456789123456789123456789123456789123456789(col_1 int,col_2 int,col_3 int);

--查看表名是否截取为63位长度
select char_length(tablename) from pg_tables where tablename like '%max_length_table%';

--清理环境
drop table max_length_table_1234567891234567891234567891234567891234567891;