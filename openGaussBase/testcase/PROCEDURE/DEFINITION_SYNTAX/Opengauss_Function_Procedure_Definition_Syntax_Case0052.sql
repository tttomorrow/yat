-- @testpoint:删除过程中的update目标表

DROP table if exists Proc_Syntax_052;
create table Proc_Syntax_052(id int,name varchar2(20));

begin
 for v_i in 1..9 loop
  insert into Proc_Syntax_052 values(v_i,'Xiaxia');
 end loop;
end;
/

select name,count(1) from Proc_Syntax_052 group by name order by name;

create or replace procedure TEST_PROC_Proc_Syntax_052(
  v_id    IN  int,
  v_name  IN  varchar2
  ) AS
  v_sql VARCHAR2(2000);
BEGIN
  update Proc_Syntax_052 set name=v_name where id=v_id;
END;
/

select name,count(1) from Proc_Syntax_052 group by name order by name;
call TEST_PROC_Proc_Syntax_052(1,'isoftstone');
select name,count(1) from Proc_Syntax_052 group by name order by name;
drop table Proc_Syntax_052;
call TEST_PROC_Proc_Syntax_052(4,'chinasoft');
select name,count(1) from Proc_Syntax_052 group by name order by name;
drop procedure TEST_PROC_Proc_Syntax_052;
