--  @testpoint:列存表使用default值
--定义一个带压缩的列存表
drop table if exists test_1;
create table test_1 (id int default 2,name char(20))WITH (ORIENTATION = COLUMN, COMPRESSION=HIGH);
insert into test_1 (name) values('lily');
select * from test_1;
drop table test_1;