-- @testpoint: circle类型转换
-- @modified at: 2020-12-3

--查询源数据类型和目标数据类型间的转化方式：
--'e'：表示只能进行显式转化（使用CAST或::语法）。
--'i'：表示只能进行隐式转化。
--'a'：表示类型间同时支持隐式和显式转化。
--转化方法：
--'f'：使用castfunc字段中指定的函数进行转化。
--'b'：类型间是二进制强制转化，不使用castfunc。
select typname,proname,castcontext,castmethod from pg_cast c
join pg_type t on t.oid=c.casttarget
left join pg_proc p on p.oid=c.castfunc
where c.oid in (select oid from pg_cast
where castsource= (select oid from pg_type where typname='circle'));

--建表
drop table if exists test_cast_0005 cascade;
create table test_cast_0005(
c_point point,
c_box box,
c_polygon polygon
);

--查询转换计划
--test point：显式转换
explain performance insert into test_cast_0005 values
(point(circle '<(1,1),2>'),box(circle '<(1.2,1.3),2.5>'),polygon(circle '<(-11.233,-10),22>'));

--清理数据
drop table if exists test_cast_0005 cascade;