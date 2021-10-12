-- @testpoint: 创建存储过程并测试execute immediate 动态查询语句

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

drop table if exists t_cust_mid;
create table t_cust_mid(
  cust_id int,
  name varchar2(200),
  user_id int,
  user_name varchar2(200),
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
  execute immediate 'drop view if exists v_cust'; 
  execute immediate 'create view v_cust as
  select cust_id, t.name, s from (select cust_id, t.name, sum(sal) s from t_cust t left join t_user t1
  on t.user_id = t1.user_id group by t.cust_id, t.name having sum(sal) > 100) t ';
end;
/

begin
   pro1(2);
end;
/

select * from v_cust order by 1,2,3;

create or replace procedure p2(v_month int) is
  v_id      int;
  v_cust_id varchar2(200);
begin
  insert into t_cust_mid
    select t.cust_id,t.name,t.user_id, t1.name, t1.sal
      from (select t.cust_id,
                   t.name,
                   t.user_id,
                   row_number() over(partition by cust_id order by user_id) rdd
              from (select *
                      from t_cust
                     where 1 = 1
                       and cust_id < 10
                       and exists (select 1 from v_cust)) t) t
      left join t_user t1
        on t.user_id = t1.user_id
     where rdd = 1;
  /*
  delete from t_cust t
   where t.rowid in (select rw
                       from (select row_number() over(partition by cust_id order by user_id) rdd,
                                    rowid rw
                               from t_cust)
                      where rdd = 1);
  commit;
  */
end;
/

begin
   p2(2);
end;
/

select * from t_cust_mid order by 1,2,3;
select * from t_cust order by 1,2,3;

drop table t_cust cascade;
drop table t_user cascade;
drop table if exists t_cust_mid cascade;
drop procedure pro1;
drop procedure p2;


