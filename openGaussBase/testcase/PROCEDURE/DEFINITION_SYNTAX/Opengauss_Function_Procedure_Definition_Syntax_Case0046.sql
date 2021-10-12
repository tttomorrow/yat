-- @testpoint:删除匿名块中的insert目标表

DROP table if exists Proc_Syntax_046;
create table Proc_Syntax_046(id int,name varchar2(20));

declare
  v_id      Proc_Syntax_046.id%TYPE;
  v_name    Proc_Syntax_046.name%type;
  v_sql VARCHAR2(2000);
BEGIN
     v_id :=5;
    v_name:='Xiaxia';
	for i in 0..9 loop
      insert into Proc_Syntax_046 values(i,v_name);
	end loop;
END;
/

select count(1) from Proc_Syntax_046;
delete from Proc_Syntax_046;
select count(1) from Proc_Syntax_046;
drop table Proc_Syntax_046;

declare
  v_id      Proc_Syntax_046.id%type;
  v_name    Proc_Syntax_046.name%type;
  v_sql VARCHAR2(2000);
BEGIN
    v_id :=5;
    v_name:='Xiaxia';
	for i in 0..9 loop
      insert into Proc_Syntax_046 values(i,v_name);
	end loop;
END;
/

select count(1) from Proc_Syntax_046;

