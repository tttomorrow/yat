-- @testpoint: 匿名块游标使用 loop循环

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300);

declare
  v_eno number(5);
  v_en  varchar2(10);
  v_sal number;
  cursor emp_cursor is
    select eno, en from t_cur_emp where sal < v_sal order by sal desc;
begin
  v_sal := 201;
  open emp_cursor;
  loop
    fetch emp_cursor
      into v_eno, v_en;
    exit when emp_cursor%notfound;
    raise notice '%,%',v_eno,v_en;
  end loop;
  close emp_cursor;
end;
/

drop table if exists t_cur_emp;
