-- @testpoint: 隐式游标使用

drop table if exists t_cur_emp;
create table t_cur_emp(eno int ,en varchar2(200),sal number);
insert into t_cur_emp values(1,'xu',100);
insert into t_cur_emp values(2,'zhang',200);
insert into t_cur_emp values(3,'li',300);

begin
    update t_cur_emp set sal = sal * 1.1 where eno in(1,2);
    if sql%found then
      raise notice 'many row find';
    else
      raise notice 'no found';
    end if;
    update t_cur_emp set sal = sal * 1.1 where eno in(2);
    if sql%found then
      raise notice 'one row find';
    else
      raise notice 'no found';
    end if;
    update t_cur_emp set sal = sal * 1.1 where eno in(3);
    if sql%found then
      raise notice 'one row find';
    else
      raise notice 'no found';
    end if;
end;
/

drop table if exists t_cur_emp;
