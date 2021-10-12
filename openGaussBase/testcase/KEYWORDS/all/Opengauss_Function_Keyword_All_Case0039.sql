-- @testpoint: 关键字all带双引号作为普通表的列名在select语句的使用
drop table if exists  test_all_003;
create table test_all_003 ("all" int);
insert into test_all_003 ("all")values(20);

select "all" from test_all_003 order by "all";
drop table if exists  test_all_003;