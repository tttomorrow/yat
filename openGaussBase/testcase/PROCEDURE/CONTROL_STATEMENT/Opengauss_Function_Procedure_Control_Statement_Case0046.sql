-- @testpoint: 匿名块异常捕获

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300);

declare
  v_name varchar2(200);
begin
  select en into v_name from t_cur_emp where eno = 1234;
exception
  when no_data_found then
    raise notice 'emp not found';
  when others then
    raise notice 'else exception';
end;
/

drop table if exists t_cur_emp;
