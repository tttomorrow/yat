--  @testpoint:创建列存表，使用blob类型，应该报错
drop table if exists test;
create table test (bb blob) with(orientation=column);