-- @testpoint: 给表中插入数据，再创建视图
-- @modified at: 2020-11-18
--建表
drop table if exists table_view_002 cascade ;
create table table_view_002(
c_id int, c_integer integer,
c_real real,c_float float, c_double integer,
c_decimal decimal(38), c_number number(38),c_number1 number,c_number2 number(20,10),c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
c_clob clob,
c_raw raw(20),c_blob blob,
c_timestamp timestamp
);
--插入数据
--查询
select count(*)from table_view_002;
--创建视图
create or replace view temp_view_002 as select c_id,c_double,c_varchar from table_view_002;
--查看视图
select count(*) from temp_view_002;
--删除视图
drop view temp_view_002;
--删表
drop table table_view_002;