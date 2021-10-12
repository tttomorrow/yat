-- @testpoint: where条件 !=,<,>,between and
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
select c_id from t_abs where abs(c_id) != 123 and c_id is not null order by c_id;
select c_id from t_abs where abs(c_id) > 20 and c_id is not null order by c_id;
select c_id from t_abs where abs(c_id) < 20 and c_id is not null order by c_id;
select c_id from t_abs where abs(c_id) between 10 and 22 and c_id is not null order by c_id;
select c_id from t_abs where abs(c_id) not between 10 and 22 and c_id is not null order by c_id;
drop table if exists t_abs;