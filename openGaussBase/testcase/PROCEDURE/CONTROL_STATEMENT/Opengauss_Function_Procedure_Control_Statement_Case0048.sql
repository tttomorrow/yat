-- @testpoint: 匿名块异常捕获

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300);

declare
  cursor emp_cursor is
    select eno, en from t_cur_emp where sal < 201 order by sal desc;
begin

  open emp_cursor;
  open emp_cursor;
  close emp_cursor;
exception
  when others then
    raise notice 'error code:%',sqlstate;
    raise notice 'error message:%',sqlerrm;
end;
/

drop table if exists t_cur_emp;
