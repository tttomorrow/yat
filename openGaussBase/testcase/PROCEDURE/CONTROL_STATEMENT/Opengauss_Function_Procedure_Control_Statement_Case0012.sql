-- @testpoint: 存储过程游标使用

drop table if exists t_cust;
create table t_cust(
  cust_id int,
  name varchar2(200),
  user_id int
);
insert into t_cust values(1,'rt',1);
insert into t_cust values(1,'rt',2);
insert into t_cust values(2,'hw',1);
insert into t_cust values(3,'zr',3);

create or replace procedure pro1(v_id int) is
  r_emp t_cust%rowtype;
  type c_type is ref cursor;
  c1 c_type;
begin
  open c1 for ' 
 select * from t_cust 
  where cust_id >=:1'
    using v_id;
  loop
    fetch c1
      into r_emp;
    exit when c1%notfound;
  end loop;
  close c1;
end;
/

begin
  pro1(2);
end;
/

drop table t_cust;
drop procedure pro1;

