-- @testpoint: 多次查询
drop table if exists t_abs;
create table t_abs(c_id int);
insert into t_abs VALUES(002);
insert into t_abs VALUES(125);
insert into t_abs VALUES(056);
insert into t_abs VALUES(089);
insert into t_abs VALUES(256);
select abs(c_id) t1,abs(c_id) t2 from t_abs where c_id is not null order by t1,t2;
drop table if exists t_abs;