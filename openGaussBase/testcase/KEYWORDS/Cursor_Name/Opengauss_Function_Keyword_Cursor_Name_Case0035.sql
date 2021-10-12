-- @testpoint: 创建一个名为cursor_test的游标
drop table if exists gg_t1;
create table gg_t1 (stu_name char(20),stu_age int,sex char(10),score int,address char(10));

insert into gg_t1 values('zhangsan',18,'boy'),('lisi',25,'boy'),('wangwu',28,'girl');
START TRANSACTION;
CURSOR cursor_test FOR SELECT * FROM gg_t1;
CLOSE cursor_test;
end;
drop table if exists gg_t1;