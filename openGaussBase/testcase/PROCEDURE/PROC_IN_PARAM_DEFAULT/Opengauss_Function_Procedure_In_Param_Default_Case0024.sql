-- @testpoint: 测试入参是所有数据类型默认值的存储过程

drop table if exists test_001;
create table test_001(
  t1 int,
  t2 integer not null,
  t3 bigint,
  t4 number default 0.2332,
  t5 number(12,2),
  t6 number(12,6),
  t7 binary_double,
  t8 decimal,
  t9 decimal(8,2),
  t10 decimal(8,4),
  t11 real,
  t12 char(4000),
  t13 char(100),
  t14 varchar(4000),
  t15 varchar(100),
  t16 varchar2(4000),
  t17 numeric,
  t19 date,
  t20 timestamp,
  t21 timestamp(6),
  t22 bool
) ;

create unique index  indx_t1 on test_001(t1);
create index indx_t2 on test_001(t2,t17,t20);


--测试入参是所有数据类型默认值的存储过程
create or replace procedure proc_in_param_default_024(
p1 in int default 13,
p2 in integer default 58813,
p4 in number default 1234567.78,
p5 in number default 12345.57,
p6 in number default 12.234568,
p7 in binary_double default 1234.67,
p8 in binary_double default 2345.78,
p9 in binary_double default 12345.57,
p10 in binary_double default 12.2346,
p11 in binary_double default 12.44,
p12 in char default 'dbce',
p13 in char default 'abcdf',
p14 in varchar default 'abcdeg',
p15 in varchar default 'ac',
p16 in varchar2 default 'ade',
p17 in numeric default 123.46,
p19 in date default '2012-08-08 00:00:00',
p20 in timestamp default '2000-02-01 15:22:21.110000',
p21 in timestamp default '2012-02-01 15:12:11.320000',
p22 in bool default 'false'
)
as
v1 test_001.t13%type;
begin
	select t13 into v1 from test_001 where (t1=p1 and t2=p2 and t3=p3 and t4=p4 and t5=p5 and t6=p6 and t7=p7 and t8=t8 and t9=p9 and t10=p10 and t11=p11 and t12=p12 and t13=p13 and t14=p14 and t15=p15 and t16=p16 and t17=p17 and t19=p19 and t20=p20 and t21=p21 and t22=p22) ;
	raise info 'v1:%',v1;
	exception
	when no_data_found 
	then 
		raise info 'no_data_found';
end;
/
--调用存储过程
begin
	proc_in_param_default_024();
end;
/
--清理环境
drop table if exists test_001;
drop procedure proc_in_param_default_024;
