-- @testpoint: 创建存储过程并测试execute immediate 动态查询语句

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
  v_int int := -1;
begin
  execute immediate 'select count(1) from t_cust where cust_id=:1'
    into v_int
    using v_id;
  raise notice '%',v_int;
end;
/

begin
   pro1(1);
   pro1(2);
   pro1(5);
end;
/

drop table t_cust;
drop procedure pro1;

