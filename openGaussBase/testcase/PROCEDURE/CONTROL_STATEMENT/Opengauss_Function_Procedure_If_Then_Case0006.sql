-- @testpoint: 条件语句if ...then ...else

drop table if exists table_if_else_006;
create table table_if_else_006(id int not null,name varchar2(32),job varchar2(32));
insert into table_if_else_006 values (1,'kobe','player'),(2,'lucy','singer'),(3,'tom','doctors');

create or replace procedure proc_if_else_0006(
  p_name      in   varchar2,
  p_job_code  out  varchar2
) as
  loginid int default 0;
begin
	select id into loginid from table_if_else_006 where name = p_name;
	if (loginid = 1)
	then
		p_job_code:='0001';
	raise info 'the job_code is 0001';
	elsif (loginid = 2)
	then
		p_job_code:='0002';
	raise info 'the job_code is 0002';
	else
		p_job_code:='0003';
	raise info 'the job_code is 0003';
	return;
	end if;
end;
/
--test调用存储过程
declare
	v_job_code varchar2(10);
begin
	proc_if_else_0006('kobe',v_job_code);
end;
/
--test调用存储过程
declare
	v_job_code varchar2(10);
begin
	proc_if_else_0006('lucy',v_job_code);
end;
/
--test调用存储过程
declare
	v_job_code varchar2(10);
begin
	proc_if_else_0006('tom',v_job_code);
end;
/
drop procedure proc_if_else_0006;
drop table if exists table_if_else_006;