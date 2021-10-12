-- @testpoint: 匿名块游标使用

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300);

declare
  v_empno int;
  v_ename varchar2(200);
  cursor emp_cursor(p_eno int) is
    select eno, en from t_cur_emp where eno <= p_eno   order by sal desc;
begin
  open emp_cursor(2);
  loop
    fetch emp_cursor
      into v_empno, v_ename;
    exit when emp_cursor%notfound;
    raise notice '%,%',v_empno,v_ename;
  end loop;
  close emp_cursor;
end;
/

drop table if exists t_cur_emp;
