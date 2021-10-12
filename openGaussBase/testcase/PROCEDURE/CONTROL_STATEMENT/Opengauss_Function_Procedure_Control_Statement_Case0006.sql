-- @testpoint: 创建存储过程并测试execute immediate 动态非查询语句

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

create or replace procedure pro1(v_month int) is
  v_name varchar2(200):='xq';
  v_user_id number:=12;
  v_id int:=1;
begin
  execute immediate 'insert into t_cust values(:1,:2,:3)
  ' using  v_month,v_name,v_user_id;
  execute immediate 'delete from t_cust where cust_id=:1
  ' using  v_id;
  v_name:='wwj';
  v_id:=2;
  execute immediate 'update t_cust t set t.name=:1 where cust_id=:2
  ' using  v_name,v_id; 
end;
/

begin
   pro1(5);
end;
/

select * from t_cust;
drop table t_cust;
drop procedure pro1;
