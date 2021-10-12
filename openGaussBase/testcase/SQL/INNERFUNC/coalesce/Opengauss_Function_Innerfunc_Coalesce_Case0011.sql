-- @testpoint:where的使用
drop table if exists t_coalesce;
create table t_coalesce(id int,numb int);
insert into t_coalesce values(1,111);
insert into t_coalesce values(2,null);
insert into t_coalesce values(3,222);
insert into t_coalesce values(4,null);
select coalesce(numb,0) from t_coalesce where coalesce(1,null,2)=1  order by id;
drop table if exists t_coalesce;