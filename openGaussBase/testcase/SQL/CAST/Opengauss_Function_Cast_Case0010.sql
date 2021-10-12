-- @testpoint: bool类型转换
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
where castsource= (select oid from pg_type where typname='bool'));

--建表
drop table if exists test_cast_0010 cascade;
create table test_cast_0010(
c_int1 int1,
c_int4 int4,
c_int2 int2,
c_int8 int8,
c_text text,
c_clob clob,
c_varchar varchar,
c_nvarchar2 nvarchar2,
c_bpchar bpchar
);

--查询转换计划
--test point：隐式转换
explain performance insert into test_cast_0010 values(
1::bool,
0::bool,
1::bool,
0::bool,
'1'::bool,
'0'::bool,
'true'::bool,
'false'::bool,
'1'::bool
);

--test point：显式转换
explain performance insert into test_cast_0010(c_text) values('t'::bool::text);
explain performance insert into test_cast_0010(c_clob) values(cast('f'::bool as clob));
explain performance insert into test_cast_0010(c_varchar) values(123456::bool::varchar);
explain performance insert into test_cast_0010(c_nvarchar2) values(cast('off'::bool as nvarchar2));
explain performance insert into test_cast_0010(c_bpchar) values('yes'::bool::bpchar);

--清理数据
drop table if exists test_cast_0010 cascade;