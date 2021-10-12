-- @testpoint:删除匿名块中的update目标表

DROP table if exists  Proc_Syntax_048;
create table Proc_Syntax_048(id int,name varchar2(20));

begin
 for v_i in 1..9 loop
  insert into Proc_Syntax_048 values(v_i,'Xiaxia');
 end loop;
end;
/

select name,count(1) from Proc_Syntax_048 group by name order by name;

declare
  v_id      int;
  v_name    varchar2(200):='isoftstone';
  v_sql VARCHAR2(2000);
BEGIN
  v_id :=4;
  update Proc_Syntax_048 set name=v_name where id=v_id;
END;
/

select name,count(1) from Proc_Syntax_048 group by name order by name;
drop table Proc_Syntax_048;

declare
  v_id      int;
  v_name    varchar2(200):='chinasoft';
  v_sql VARCHAR2(2000);
BEGIN
   v_id :=4;
  update Proc_Syntax_048 set name=v_name where id=v_id;
END;
/

select name,count(1) from Proc_Syntax_048 group by name order by name;
DROP table   Proc_Syntax_048;


