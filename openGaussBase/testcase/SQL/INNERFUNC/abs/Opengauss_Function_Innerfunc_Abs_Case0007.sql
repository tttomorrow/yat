-- @testpoint: where条件is [not] null,[not] in,[not] exists
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
select c_id from t_abs where abs(c_id) in (11,22) and c_id is not null order by c_id;
select c_id from t_abs where abs(c_id) not in (11,22) and c_id is not null order by c_id;
select c_id from t_abs where abs(c_id) is null order by c_id;
select c_id from t_abs where abs(c_id) is not null order by c_id;
select abs(c_id) t1 from t_abs where c_id is not null and exists (select abs(c_id) from t_abs where c_id is not null) order by t1;
select abs(c_id) t1 from t_abs where c_id is not null and not exists (select abs(c_id) from t_abs where c_id is not null) order by t1;
drop table if exists t_abs;