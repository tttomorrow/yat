-- @testpoint: inet类型转换
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
where castsource= (select oid from pg_type where typname='inet'));

--建表
drop table if exists test_cast_0011 cascade;
create table test_cast_0011(
c_cidr cidr,
c_text text,
c_clob clob,
c_varchar varchar,
c_nvarchar2 nvarchar2,
c_bpchar bpchar
);

--查询转换计划
--test point：隐式转换
--ipv4
insert into test_cast_0011 values('0.0.0.0/24','0.0.0.0/24','0.0.0.0/24','0.0.0.0/24','0.0.0.0/24','0.0.0.0/24');
--ipv6
insert into test_cast_0011 values('2001:4f8:3:ba::/64','2001:4f8:3:ba::/64','2001:4f8:3:ba::/64','2001:4f8:3:ba::/64','2001:4f8:3:ba::/64','2001:4f8:3:ba::/64');


--test point：显式转换
--ipv4
explain performance insert into test_cast_0011 values(
cast(inet '0.0.0.0/24' as cidr),'11.11.11.11'::inet::text,cast('11.11.11.11'::inet as clob),
'11.11.11.11'::inet::varchar,cast('11.11.11.11'::inet as nvarchar2),'11.11.11.11'::inet::bpchar);
--ipv6
explain performance insert into test_cast_0011 values(
cast(inet '2001:4f8:3:ba::/64' as cidr),'2001:4f8:3:ba::/64'::inet::text,cast('2001:4f8:3:ba::/64'::inet as clob),
'2001:4f8:3:ba::/64'::inet::varchar,cast('2001:4f8:3:ba::/64'::inet as nvarchar2),'2001:4f8:3:ba::/64'::inet::bpchar);

--清理数据
drop table if exists test_cast_0011 cascade;