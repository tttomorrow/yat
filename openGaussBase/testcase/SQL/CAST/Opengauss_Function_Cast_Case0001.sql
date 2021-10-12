-- @testpoint: 二进制类型：blob类型转换

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
where castsource= (select oid from pg_type where typname='blob'));

--建表
drop table if exists test_cast_0001 cascade;
create table test_cast_0001(c_raw raw);

--查询转换计划
--test point：隐式转换
explain performance insert into test_cast_0001 values(HEXTORAW('DEADBEEF')::blob);

--清理数据
drop table if exists test_cast_0001 cascade;