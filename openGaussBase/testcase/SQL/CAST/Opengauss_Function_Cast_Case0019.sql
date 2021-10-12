-- @testpoint: bit类型转换

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
where castsource= (select oid from pg_type where typname='bit'));

--建表
drop table if exists test_cast_0019 cascade;
create table test_cast_0019(
c_varbit varbit,
c_int8 int8,
c_int4 int4,
c_bit bit
);

--查询转换计划
--test point：隐式转换:success
explain performance insert into test_cast_0019(c_varbit,c_bit) values(B'101',B'1');

--test point：显式转换:success
explain performance insert into test_cast_0019(c_int8) values(B'10101'::bit::int8);
explain performance insert into test_cast_0019(c_int4) values(cast(B'101'::bit as int4));

--清理数据
drop table if exists test_cast_0019 cascade;