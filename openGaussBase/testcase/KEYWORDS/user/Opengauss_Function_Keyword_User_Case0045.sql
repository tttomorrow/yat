-- @testpoint: 结合where查询列的值是user，部分测试点合理报错
drop table if exists user_06;
create table user_06(name varchar(13),school varchar(13));
insert into user_06 values('李明','sys');
insert into user_06 values('张三','user');
insert into user_06 values('小红','de');
select * from user_06;
select * from user_06 where school='user';
drop table if exists user_06;