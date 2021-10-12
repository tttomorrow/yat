-- @testpoint: varchar类型转换

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
where castsource= (select oid from pg_type where typname='varchar'));

--建表
drop table if exists test_cast_0002 cascade;
create table test_cast_0002(
c_char char,
c_name name,
c_int8 int8,
c_int4 int4,
c_text text,
c_float4 float4,
c_float8 float8,
c_bpchar bpchar,
c_varchar varchar,
c_nvarchar2 nvarchar2,
c_date date,
c_timestamp timestamp,
c_interval interval,
c_numeric numeric,
c_regclass regclass,
c_smalldatetime smalldatetime,
c_raw raw,
c_clob clob
);

--查询转换计划
--test point：隐式转换
explain performance insert into test_cast_0002 values(
't'::varchar,
'test_cast_0002'::varchar,
'0002'::varchar,
'0002'::varchar,
'test_cast_0002'::varchar,
'0.0002'::varchar,
'0.0002'::varchar,
'test_cast_0002'::varchar,
'test_cast_0002'::varchar,
'test_cast_0002'::varchar,
'2020-09-28'::varchar,
'2020-09-28'::varchar,
'10'::varchar,
'1.0002'::varchar,
'test_cast_0002'::varchar,
'2020-09-28'::varchar,
HEXTORAW('DEADBEEF')::varchar,
'test_cast_0002'::varchar
);

--test point：显式转换
explain performance insert into test_cast_0002(c_char) values(cast('t'::varchar as char));

--清理数据
drop table if exists test_cast_0002 cascade;