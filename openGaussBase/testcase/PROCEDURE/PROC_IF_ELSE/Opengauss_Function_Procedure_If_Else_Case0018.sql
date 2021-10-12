-- @testpoint: 测试带有动态语句的if/else语句

drop table if exists PROC_IF_ELSE_001;
create table PROC_IF_ELSE_001(id int not null,name varchar2(32),job varchar2(32));
insert into PROC_IF_ELSE_001 values (1,'kobe','player'),(2,'lucy','singer'),(3,'tom','doctors');

--创建存储过程
create or replace procedure PROC_IF_ELSE_018(
  p_name      in   varchar2,
  p_job_code  out  varchar2
) AS
  LoginId INT default 0;
begin
	select id into LoginId from PROC_IF_ELSE_001 where name = p_name;
	IF (LoginId = 1)
	THEN
	    p_job_code:='0001';
	    raise info 'the job_code is 0001';
	    elsif (LoginId = 2)
	THEN
	    p_job_code:='0002';
	    raise info 'the job_code is 0002';
	ELSE
	    p_job_code:='0003';
	    raise info 'the job_code is 0003';
	    return;
	END IF;
end;
/
--调用存储过程
DECLARE
    v_job_code varchar2(10);
BEGIN
    PROC_IF_ELSE_018('kobe',v_job_code);
END;
/
--调用存储过程
DECLARE
    v_job_code varchar2(10);
BEGIN
    PROC_IF_ELSE_018('lucy',v_job_code);
END;
/
--调用存储过程
DECLARE
    v_job_code varchar2(10);
BEGIN
    PROC_IF_ELSE_018('tom',v_job_code);
END;
/
--清理环境
drop procedure PROC_IF_ELSE_018;
drop table if exists PROC_IF_ELSE_001;