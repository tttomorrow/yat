-- @testpoint: right函数与where结合
drop table if exists t_concat;
create table t_concat(id int,v_char varchar(10));
insert into t_concat values(1,'awsdaw');
select id,right(v_char,2) from t_concat where ascii(v_char) in (97,98) order by id;
drop table if exists t_concat;