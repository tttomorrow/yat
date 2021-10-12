-- @testpoint: 存储过程使用序列

drop table if exists t_cust;
drop sequence if exists seq_t001;
drop sequence if exists seq_t002;
drop sequence if exists seq_t003;
drop table if exists test_seq_table_01;
drop table if exists test_seq_table_02;
drop table if exists test_seq_table_03;
create table t_cust(
  cust_id int,
  name varchar2(200),
  user_id int
);
insert into t_cust values(1,'rt',1);
insert into t_cust values(1,'rt',2);
insert into t_cust values(1,'rt',3);
insert into t_cust values(2,'hw',1);
insert into t_cust values(3,'zr',2);
insert into t_cust values(4,'zr',2);
insert into t_cust values(5,'zr',2);
insert into t_cust values(10,'zr',2);

create sequence seq_t001 increment by 1 start with 10001;
create sequence seq_t002 increment by 2 start with 20001;
create sequence seq_t003 increment by 5 start with 30001;

create or replace procedure p002(v_id int) is
begin
  execute immediate 'create table test_seq_table_01 as select seq_t001.nextval as b,seq_t002.nextval as b1,seq_t003.nextval as b2 from sys_dummy';
  execute immediate 'create table test_seq_table_02 as select seq_t001.nextval as id,seq_t002.nextval as b1,seq_t003.nextval as b2,
  cust_id,name,user_id from t_cust where cust_id<=5';
  execute immediate 'create table test_seq_table_03 as select seq_t001.nextval as id,seq_t002.nextval as b1,seq_t003.nextval as b2,seq_t001.nextval as id1,
  cust_id,name,user_id from t_cust where cust_id<= '||v_id;
end;
/

call p002(4);

select * from test_seq_table_01 order by b;
select * from test_seq_table_02 order by id;
select * from test_seq_table_03 order by id;

drop table if exists t_cust;
drop table test_seq_table_01;
drop table test_seq_table_02;
drop table test_seq_table_03;
drop sequence if exists seq_t001;
drop sequence if exists seq_t002;
drop sequence if exists seq_t003;
drop procedure p002;


    
