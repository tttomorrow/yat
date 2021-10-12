-- @testpoint: box类型转换
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
where castsource= (select oid from pg_type where typname='box'));

--建表
drop table if exists test_cast_0006 cascade;
create table test_cast_0006(
c_point point,
c_lseg lseg,
c_circle circle,
c_polygon polygon
);

--查询转换计划
--test point：隐式转换
explain performance insert into test_cast_0006(c_polygon) values(polygon '(1,1),(2,2),(3,3),(4,4)');

--test point：显式转换
explain performance insert into test_cast_0006 values(point(box('5,5,6,6')),lseg(box'(1,2),(3,2)'),circle(box('(1,1),(5,6)')),polygon(box'(0.1,0.1),(3.2,3.3)'));

--清理数据
drop table if exists test_cast_0006 cascade;