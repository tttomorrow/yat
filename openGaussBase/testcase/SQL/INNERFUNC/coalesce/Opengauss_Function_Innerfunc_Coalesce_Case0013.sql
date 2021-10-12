-- @testpoint:创建视图
drop table if exists t_coalesce;
create table t_coalesce(id int,numb int);
insert into t_coalesce values(1,111);
insert into t_coalesce values(2,null);
insert into t_coalesce values(3,222);
insert into t_coalesce values(4,null);
create or replace view v_t_coalesce as select numb from t_coalesce;
select coalesce(numb,0) from v_t_coalesce order by numb;
drop view v_t_coalesce;
drop table if exists t_coalesce;