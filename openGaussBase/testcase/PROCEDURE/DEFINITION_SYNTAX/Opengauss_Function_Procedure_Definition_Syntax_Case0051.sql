-- @testpoint:删除过程中的select原表

DROP table if exists Proc_Syntax_051;
drop table if exists  Proc_Syntax_051_mid;
create table Proc_Syntax_051(id int,name varchar2(20));
create table Proc_Syntax_051_mid(id int,name varchar2(20));

begin
 for v_i in 1..9 loop
  insert into Proc_Syntax_051_mid values(v_i,'Xiaxia');
 end loop;
end;
/

select count(1) from Proc_Syntax_051_mid;

create or replace procedure TEST_PROC_Proc_Syntax_051(
  v_id    IN  int,
  v_name  IN  varchar2
  ) AS
  v_sql VARCHAR2(2000);
BEGIN
  insert into Proc_Syntax_051
  select * from Proc_Syntax_051_mid;

END;
/

select count(1) from Proc_Syntax_051;
call TEST_PROC_Proc_Syntax_051(1,'Xiaxia1');
select count(1) from Proc_Syntax_051;
drop table  Proc_Syntax_051_mid;
call TEST_PROC_Proc_Syntax_051(4,'Xiaxia4');
select count(1) from Proc_Syntax_051;
drop procedure TEST_PROC_Proc_Syntax_051;
drop table Proc_Syntax_051;
