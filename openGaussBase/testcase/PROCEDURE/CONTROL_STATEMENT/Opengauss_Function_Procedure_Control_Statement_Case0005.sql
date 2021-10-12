-- @testpoint: 存储过程测试execute immediate 动态查询

drop table if exists t_cust;
create table t_cust(
  cust_id int,
  name varchar2(200),
  user_id int
);
drop table if exists t_user;
create table t_user(
  user_id int,
  name varchar2(200),
  sal number
);
insert into t_cust values(1,'rt',1);
insert into t_cust values(1,'rt',2);
insert into t_cust values(1,'rt',3);
insert into t_cust values(2,'hw',1);
insert into t_cust values(3,'zr',2);

insert into t_user values(1,'xq',900);
insert into t_user values(2,'ll',900);
insert into t_user values(3,'wwj',900);
insert into t_user values(1,'xq',899.99);

create or replace procedure pro1(v_month int) is
  v_id int;
  v_cust_id varchar2(200);
begin
  execute immediate 'select t.name, s
  from (select cust_id, t.name, sum(sal) s
          from t_cust t
          left join t_user t1
            on t.user_id = t1.user_id
         group by t.cust_id, t.name
        having sum(sal) > 100) t
  where s > 2000
  order by t.cust_id'
      into v_cust_id,v_id;
end;
/

begin
   pro1(2);
end;
/

drop table t_cust;
drop table t_user;
drop procedure pro1;


