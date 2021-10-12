-- @testpoint: sign函数在创建视图时使用
drop view if exists v_sign;
drop table if exists test_sign;
create table test_sign(a int,b float);
insert into test_sign values(1,-0.1),(2,123.986),(3,-6999.7);
create or replace view v_sign as select a,sign(b) from test_sign;
select * from v_sign order by a;
drop view v_sign;
drop table test_sign;