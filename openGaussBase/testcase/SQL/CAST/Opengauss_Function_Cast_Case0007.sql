-- @testpoint: int2类型转换

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
where castsource= (select oid from pg_type where typname='int2'));

--建表
drop table if exists test_cast_0007 cascade;
create table test_cast_0007(
c_int1 int1,
c_int8 int8,
c_int4 int4,
c_float4 float4,
c_float8 float8,
c_numeric numeric,
c_bool bool,
c_interval interval,
c_oid oid,
c_regproc regproc,
c_regprocedure regprocedure,
c_regoper regoper,
c_regoperator regoperator,
c_regclass regclass,
c_regtype regtype,
c_regconfig regconfig,
c_regdictionary regdictionary,
c_text text,
c_clob clob,
c_varchar varchar,
c_bpchar bpchar,
c_nvarchar2 nvarchar2
);

--查询转换计划
--test point：隐式转换
explain performance insert into test_cast_0007 values(
7::int2,
7::int2,
7::int2,
1.0007::int2,
1.0007::int2,
1.0007::int2,
1::int2,
7::int2,
7::int2,
7::int2,
7::int2,
7::int2,
7::int2,
7::int2,
7::int2,
7::int2,
7::int2,
'0007'::int2,
'0007'::int2,
'0007'::int2,
'0007'::int2,
'0007'::int2
);

--清理数据
drop table if exists test_cast_0007 cascade;