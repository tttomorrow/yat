-- @testpoint: 匿名块异常捕获

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300);

declare
  v_eno varchar2(20);
  v_en  varchar2(200);
  cursor emp_cursor is
    select eno, en from t_cur_emp where sal < 201 order by sal desc;
begin
  fetch emp_cursor
    into v_eno, v_en;

exception
  when others then
    raise notice 'error code:%',sqlstate;
    raise notice 'error message:%',sqlerrm;
end;
/

drop table if exists t_cur_emp;
