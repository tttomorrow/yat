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

create or replace procedure pro1(v_id int,v_name varchar2,v_m out int) is
begin
  execute immediate 'select count(1) from t_cust where cust_id=:1'
    into v_m
    using v_id;
end;
/

declare
  v_proc varchar2(100) := 'pro1';
  v_id   int := 1;
  v_name varchar2(200) := 'xuqiang';
  v_m    int;
begin
  execute immediate 'begin ' || v_proc || '(:2, :3, :4); end;'
  using  v_id, in v_name, out v_m;
  raise notice '%',v_m;
end;
/

drop table t_cust;
drop procedure pro1;



