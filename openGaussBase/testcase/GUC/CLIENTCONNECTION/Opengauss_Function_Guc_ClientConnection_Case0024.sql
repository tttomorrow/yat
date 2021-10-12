-- @testpoint: 设置current_schema为不存在的模式，建表，合理报错
set current_schema to kkkurtyu;
--查询
show current_schema;
--建表，报错
drop table if exists test_search_path024;
create table test_search_path024(id int);
--恢复默认
set current_schema to public;
show current_schema;