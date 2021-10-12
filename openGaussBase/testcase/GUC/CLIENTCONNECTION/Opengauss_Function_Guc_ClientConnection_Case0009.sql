-- @testpoint: 设置参数search_path为其他模式，不带模式，查询成功
--查看默认值
show search_path;
--创建模式
drop schema if exists t_myschema009 cascade;
create schema t_myschema009;
--建表
drop table if exists t_myschema009.test_search_path009;
create table t_myschema009.test_search_path009(id int);
--插入数据
insert into t_myschema009.test_search_path009 values(2);
--将新模式放入搜索路径中
set search_path to "$user",public,t_myschema009;
--查询
show search_path;
--不带模式，查询,成功
select * from test_search_path009;
--带模式，查询,成功
select * from t_myschema009.test_search_path009;
--清理环境
drop table if exists t_myschema009.test_search_path009;
drop schema if exists t_myschema009 cascade;
set search_path to "$user",public;