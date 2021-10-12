-- @testpoint: pg_node_tree类型转换 --表达式树
-- @modified at: 2020-12-3

--查询源数据类型和目标数据类型间的转化方式：
--'e'：表示只能进行显式转化（使用CAST或::语法）。
--'i'：表示只能进行隐式转化。
--'a'：表示类型间同时支持隐式和显式转化。
--转化方法：
--'f'：使用castfunc字段中指定的函数进行转化。
--'b'：类型间是二进制强制转化，不使用castfunc。
select typname,proname,castcontext,castmethod,proargdefaults from pg_cast c
join pg_type t on t.oid=c.casttarget
left join pg_proc p on p.oid=c.castfunc
where c.oid in (select oid from pg_cast
where castsource= (select oid from pg_type where typname='pg_node_tree'));

--建表
drop table if exists test_cast_0020 cascade;
create table test_cast_0020(
c_text text,
c_clob clob
);

--查询转换计划
--test point：隐式转换
explain performance insert into test_cast_0020 values(
'({CONST :consttype 2275 :consttypmod -1 :constcollid 0 :constlen -2 :constbyval false :constisnull false :ismaxvalue false :location 217538 :constvalue 1 [ 0 ] :cursor_data  :row_count 0 :cur_dno 0 :is_open false :found false :not_found false :null_open false :null_fetch false})',
'({CONST :consttype 2275 :consttypmod -1 :constcollid 0 :constlen -2 :constbyval false :constisnull false :ismaxvalue false :location 217538 :constvalue 1 [ 0 ] :cursor_data  :row_count 0 :cur_dno 0 :is_open false :found false :not_found false :null_open false :null_fetch false})');


--清理数据
drop table if exists test_cast_0020 cascade;