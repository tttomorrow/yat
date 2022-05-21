-- @testpoint: NVARCHAR(n)类型转换测试  部分测试点合理报错

--step1:建表; expect:成功
drop table if exists t_nvarchar_0004 cascade;
create table t_nvarchar_0004(
c_nvarchar nvarchar,
c_nvarchar2 nvarchar2,
c_text text,
c_clob clob,
c_bpchar bpchar,
c_varchar varchar,
c_char char,
c_name name,
c_bool bool,
c_timestamp timestamp,
c_int4 int4,
c_numeric numeric
);

--step2:转换为nvarchar; expect:成功
--隐式转化
insert into t_nvarchar_0004(c_nvarchar) values('text'::text);
insert into t_nvarchar_0004(c_nvarchar) values('clob'::clob);
insert into t_nvarchar_0004(c_nvarchar) values('varchar'::varchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('bpchar'::bpchar));
insert into t_nvarchar_0004(c_nvarchar) values('nvarchar');
insert into t_nvarchar_0004(c_nvarchar) values(int1_nvarchar2(12::int1));
insert into t_nvarchar_0004(c_nvarchar) values(to_nvarchar2('12345'::int2));
insert into t_nvarchar_0004(c_nvarchar) values(to_nvarchar2('12345'::int4));
insert into t_nvarchar_0004(c_nvarchar) values(to_nvarchar2('12345'::int8));
insert into t_nvarchar_0004(c_nvarchar) values(to_nvarchar2('123.45'::numeric));
insert into t_nvarchar_0004(c_nvarchar) values(to_nvarchar2('2000-01-01 00:00:00'::timestamp));
insert into t_nvarchar_0004(c_nvarchar) values(to_nvarchar2('MONTH 5'::interval));
insert into t_nvarchar_0004(c_nvarchar) values(to_nvarchar2('2.4'::float4));
insert into t_nvarchar_0004(c_nvarchar) values(to_nvarchar2('2.8'::float8));
--同时支持隐式和显式转化
--隐式
insert into t_nvarchar_0004(c_nvarchar) values(text('char'::char(4)));
insert into t_nvarchar_0004(c_nvarchar) values(text('192.168.100.128/25'::cidr));
insert into t_nvarchar_0004(c_nvarchar) values(text('127.0.0.1'::cidr));
insert into t_nvarchar_0004(c_nvarchar) values(text('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr));
insert into t_nvarchar_0004(c_nvarchar) values(text('192.168.100.128/25'::inet));
insert into t_nvarchar_0004(c_nvarchar) values(text('127.0.0.1'::inet));
insert into t_nvarchar_0004(c_nvarchar) values(text('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::inet));
insert into t_nvarchar_0004(c_nvarchar) values(text('true'::bool));
insert into t_nvarchar_0004(c_nvarchar) values(text('1'::bool));
insert into t_nvarchar_0004(c_nvarchar) values(text('yes'::bool));
insert into t_nvarchar_0004(c_nvarchar) values(text('false'::bool));
insert into t_nvarchar_0004(c_nvarchar) values(text('0'::bool));
insert into t_nvarchar_0004(c_nvarchar) values(text('no'::bool));
--显式
insert into t_nvarchar_0004(c_nvarchar) values(text('char'::char(4)::nvarchar));
insert into t_nvarchar_0004(c_nvarchar) values(text('192.168.100.128/25'::cidr)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('10'::cidr)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::cidr)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('192.168.100.128/25'::inet)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('192.168.100.128/25'::inet)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('2001:4f8:3:ba:2e0:81ff:fe22:d1f1/128'::inet)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('true'::bool)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('1'::bool)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('yes'::bool)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('false'::bool)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('0'::bool)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values(text('no'::bool)::nvarchar);
insert into t_nvarchar_0004(c_nvarchar) values('name'::name::nvarchar);

--step3:nvarchar转换为其他类型; expect:成功
insert into t_nvarchar_0004(c_nvarchar2) values('nvarchar2'::nvarchar);
insert into t_nvarchar_0004(c_char) values('c'::nvarchar);
insert into t_nvarchar_0004(c_text) values('text'::nvarchar);
insert into t_nvarchar_0004(c_clob) values('clob'::nvarchar);
insert into t_nvarchar_0004(c_bpchar) values('bpchar'::nvarchar);
insert into t_nvarchar_0004(c_varchar) values('varchar'::nvarchar);
insert into t_nvarchar_0004(c_numeric) values(to_numeric('2.44'::nvarchar));
insert into t_nvarchar_0004(c_int4) values(to_integer('44'::nvarchar));
insert into t_nvarchar_0004(c_timestamp) values(to_ts('2001-01-01 00:00:00'::nvarchar));
insert into t_nvarchar_0004(c_name) values(name('name'::nvarchar));

--step4:nvarchar不支持的类型转换; expect:合理报错
insert into t_nvarchar_0004(c_nvarchar) values( '2001-01-01'::time);

--step5:清理环境; expect:成功
drop table if exists t_nvarchar_0004 cascade;