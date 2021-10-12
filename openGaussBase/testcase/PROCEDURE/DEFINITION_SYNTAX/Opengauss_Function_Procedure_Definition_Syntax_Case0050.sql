-- @testpoint:删除过程中的insert目标表

DROP table if exists Proc_Syntax_050;
create table Proc_Syntax_050(id int,name varchar2(20));

create or replace procedure TEST_PROC_Proc_Syntax_050(
  v_id    IN  Proc_Syntax_050.id%type,
  v_name  IN  Proc_Syntax_050.name%type
  ) AS
  v_sql VARCHAR2(2000);
BEGIN
    insert into Proc_Syntax_050 values(v_id,v_name);
END;
/

select count(1) from Proc_Syntax_050;
call TEST_PROC_Proc_Syntax_050(3,'isoft');

select count(1) from Proc_Syntax_050;
drop table Proc_Syntax_050;
call TEST_PROC_Proc_Syntax_050(4,'isoft');
select count(1) from Proc_Syntax_050;
drop procedure TEST_PROC_Proc_Syntax_050;



