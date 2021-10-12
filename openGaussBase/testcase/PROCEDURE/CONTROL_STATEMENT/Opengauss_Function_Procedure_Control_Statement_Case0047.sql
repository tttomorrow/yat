-- @testpoint: 匿名块异常捕获

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300)
;
declare
  v_temp number(5) := 1;
begin
  v_temp := v_temp / 0;
exception
  when others then
    raise notice 'system error';
    raise notice 'error code:%',sqlstate;
    raise notice 'error message:%',sqlerrm;
end;
/

drop table if exists t_cur_emp;
