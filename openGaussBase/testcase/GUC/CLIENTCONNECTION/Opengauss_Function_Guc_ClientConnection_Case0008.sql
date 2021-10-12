-- @testpoint: 未将新模式加入参数search_path，不带模式查询，合理报错
--查看默认值
show search_path;
--创建模式
drop schema if exists t_myschema008 cascade;
create schema t_myschema008;
--建表
drop table if exists t_myschema008.test_search_path008;
create table t_myschema008.test_search_path008(id int);
--插入数据
insert into t_myschema008.test_search_path008 values(2);
--不带模式，查询，报错
select * from test_search_path008;
--清理环境
drop table if exists t_myschema008.test_search_path008;
drop schema if exists t_myschema008 cascade;