-- @testpoint:删除匿名块中的delete目标表

DROP table if exists  Proc_Syntax_049;
create table Proc_Syntax_049(id int,name varchar2(20));

begin
 for v_i in 1..9 loop
  insert into Proc_Syntax_049 values(v_i,'Xiaxia');
 end loop;
end;
/

select name,count(1) from Proc_Syntax_049 group by name order by name;

declare 
  v_id      int:=8;
  v_name    varchar2(200);
  v_sql VARCHAR2(2000);
BEGIN
  delete from Proc_Syntax_049 where id=v_id;
END;
/

select name,count(1) from Proc_Syntax_049 group by name order by name;
drop table Proc_Syntax_049;

declare 
   v_id      int:=8;
  v_name    varchar2(200);
  v_sql VARCHAR2(2000);
BEGIN
  delete from Proc_Syntax_049 where id=v_id;
END;
/

select name,count(1) from Proc_Syntax_049 group by name order by name;
drop table Proc_Syntax_049;

