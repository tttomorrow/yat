-- @testpoint: 测试入参为char default的存储过程

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


--创建存储过程
create or replace procedure proc_in_param_default_0013(p1 in char default 'abcdf') 
as
v1 test_001.t1%type;
begin
	select t1 into v1 from test_001 where t13=p1;
	raise info 'v1:%',v1;
	exception
	when no_data_found 
	then 
		raise info 'no_data_found';
end;
/
--调用存储过程
begin
	proc_in_param_default_0013();
end;
/
--清理环境
drop table if exists test_001;
drop procedure proc_in_param_default_0013;

