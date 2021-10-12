-- @testpoint: 条件语句 if ...then ...else

drop table if exists proc_if_else_007;
create table proc_if_else_007(id int not null,name varchar2(32),job varchar2(32));
insert into proc_if_else_007 values (1,'kobe','player'),(2,'lucy','singer'),(3,'tom','doctors');

create or replace procedure proc_if_else_00_8(
  p_name      in   varchar2,
  p_job_code  out  varchar2
) as
  loginid int default 0;
begin
	select id into loginid from proc_if_else_007 where name = p_name;
	if (loginid = 1)
	then
	p_job_code:='0001';
	raise info 'the job_code is 0001';
	elseif (loginid = 2)
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

declare
	v_job_code varchar2(10);
begin
	proc_if_else_00_8('kobe',v_job_code);
end;
/

declare
	v_job_code varchar2(10);
begin
	proc_if_else_00_8('lucy',v_job_code);
end;
/

declare
	v_job_code varchar2(10);
begin
	proc_if_else_00_8('tom',v_job_code);
end;
/

drop procedure proc_if_else_00_8;
drop table if exists proc_if_else_007;