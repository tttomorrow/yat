-- @testpoint: 匿名块中for loop

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300);

declare
  v_ename varchar2(200);
  v_sal   number;
  cursor emp_cursor is
    select en, sal from t_cur_emp where eno < 10 order by sal desc;
begin
  open emp_cursor;
  if emp_cursor%isopen then
    loop
      fetch emp_cursor
        into v_ename, v_sal;
      exit when emp_cursor%notfound;
      raise notice '%-%-%',to_char(emp_cursor%rowcount),v_ename,v_sal;
    end loop;
  else
    raise notice 'emp_cusrsor is not open';
  end if;
  close emp_cursor;
end;
/

drop table if exists t_cur_emp;