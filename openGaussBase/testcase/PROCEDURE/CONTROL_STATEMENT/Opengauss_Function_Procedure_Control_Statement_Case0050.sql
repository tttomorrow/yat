-- @testpoint: 匿名块异常捕获

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300);

declare
  v_en varchar2(10);
  t_not_exists exception;
begin
  execute immediate 'select e_no  from t_cur_emp_seews '
    into v_en;
  raise notice 'succ';
exception
  when t_not_exists then
    raise notice 'table not exists';
    raise notice 'error code:%',sqlstate;
    raise notice 'error message:%',sqlerrm;
  when others then
    raise notice 'else error';
    raise notice 'error code:%',sqlstate;
    raise notice 'error message:%',sqlerrm;
end;
/

drop table if exists t_cur_emp;
