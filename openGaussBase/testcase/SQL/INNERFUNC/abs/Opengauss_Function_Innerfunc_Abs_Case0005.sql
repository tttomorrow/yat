-- @testpoint: 与distinct,count结合使用
drop table if exists t_abs;
create table t_abs(c_id int);
insert into t_abs VALUES(002);
insert into t_abs VALUES(125);
insert into t_abs VALUES(056);
insert into t_abs VALUES(089);
insert into t_abs VALUES(256);
insert into t_abs VALUES(089);
insert into t_abs VALUES(256);
insert into t_abs VALUES(123);
select distinct abs(c_id) t1 from t_abs where c_id is not null order by t1;
select count(abs(c_id)) from t_abs;
drop table if exists t_abs;