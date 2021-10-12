-- @testpoint: 排序时，使用as列
drop table if exists test_as_009;
create table test_as_009 ("as" char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');
insert into test_as_009("as") values('zhangsan');
insert into test_as_009("as") values('lisi');
select * from  test_as_009 order by "as";
drop table if exists test_as_009;