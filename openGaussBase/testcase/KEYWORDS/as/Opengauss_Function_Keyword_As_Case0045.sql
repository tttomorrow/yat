--  @testpoint:定义as列带单引号，应该报错
drop table if exists test_as_011 ;
create table test_as_011 ('as' char(20),stu_age int,sex char(10),score int,address char(10) default 'gauss');