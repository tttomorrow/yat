-- @testpoint: 关键字all带双引号作为普通表的列名在delete语句的使用
drop table if exists  test_all_005 CASCADE;
create table  test_all_005("all" int);
start transaction;
insert into test_all_005 values (20);
select "all" from test_all_005 order by "all";
delete from test_all_005 where"all" = 20;
select "all" from test_all_005 order by "all";
drop table test_all_005;
commit;