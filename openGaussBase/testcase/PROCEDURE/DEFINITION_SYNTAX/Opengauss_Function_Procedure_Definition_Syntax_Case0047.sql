-- @testpoint:删除匿名块中的select原表

DROP table if exists Proc_Syntax_047;
DROP table if exists Proc_Syntax_047_mid;
create table Proc_Syntax_047(id int,name varchar2(20));
create table Proc_Syntax_047_mid(id int,name varchar2(20));

begin
    for i in 0..9 loop
      insert into Proc_Syntax_047_mid values(i,'Xiaxia');
    end loop;
end;
/

select count(1) from Proc_Syntax_047;

declare
   v_id      int;
  v_name    varchar2(200);
  v_sql VARCHAR2(2000);
BEGIN
    v_id :=5;
    v_name:='Xiaxia';
    insert into Proc_Syntax_047
	select * from Proc_Syntax_047_mid;
END;
/

select count(1) from Proc_Syntax_047;
drop table Proc_Syntax_047_mid;

declare
  v_id      int;
  v_name    varchar2(200);
  v_sql VARCHAR2(2000);
BEGIN
    v_id :=5;
    v_name:='Xiaxia';
    insert into Proc_Syntax_047
	select * from Proc_Syntax_047_mid;
END;
/

select count(1) from Proc_Syntax_047;
drop table Proc_Syntax_047;