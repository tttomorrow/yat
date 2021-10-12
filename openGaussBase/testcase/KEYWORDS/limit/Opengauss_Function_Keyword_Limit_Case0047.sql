--  @testpoint:使用关键字limit为列名的临时表创建视图
drop table if exists test_temporary_limit_007;
create temporary table test_temporary_limit_007("limit" int);
insert into test_temporary_limit_007 values(1);
create or replace view v_limit_002 as select "limit" from test_temporary_limit_007;
select "limit" from test_temporary_limit_007 order by "limit";