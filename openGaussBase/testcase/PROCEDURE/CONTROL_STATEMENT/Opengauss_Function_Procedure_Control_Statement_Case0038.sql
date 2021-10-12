-- @testpoint: 匿名块使用游标循环

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300);

declare
  cursor emp_cursor is
    select eno, en, sal from t_cur_emp where eno < 10 order by sal desc;
  emp_record emp_cursor%rowtype;
begin
  for emp_record in emp_cursor loop
    raise notice '%,%,%',emp_record.eno,emp_record.en,emp_record.sal;
  end loop;
end;
/

drop table if exists t_cur_emp;
