-- @testpoint: 匿名块使用游标

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300);

declare
  cursor emp_cursor is select eno, en, sal from t_cur_emp where eno < 10;
  emp_record emp_cursor%rowtype;
begin
  open emp_cursor;
  fetch emp_cursor into emp_record;
  raise notice '%,%,%',emp_record.eno,emp_record.en,emp_record.sal;
  close emp_cursor;
end;
/

drop table if exists t_cur_emp;
