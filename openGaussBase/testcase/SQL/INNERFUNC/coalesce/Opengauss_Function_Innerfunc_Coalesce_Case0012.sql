-- @testpoint:having的使用
drop table if exists t_coalesce;
create table t_coalesce(id int,numb int);
insert into t_coalesce values(1,111);
insert into t_coalesce values(3,222);
select sum(numb) from t_coalesce having coalesce(1,null,2)=1;
drop table if exists t_coalesce;