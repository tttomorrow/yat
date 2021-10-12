-- @testpoint: 检测是否支持列存表、内存表建立外键：合理报错
--列存合理报错,内存表不支持分区表
drop table if exists pstudent_table_07;
drop table if exists pclass_table_07;
drop table if exists pteacher_table_07;

create table pclass_table_07
(
    c_date TIMESTAMP ,
    c_name varchar not null
)with (orientation=column) partition by range(c_date)  (
  partition part1 values less than ('1990-07-07 00:00:00'));

create table pteacher_table_07
(
    t_date TIMESTAMP primary key,
    t_name varchar not null
) with (orientation=column) partition by range(t_date)  (
  partition part1 values less than ('1990-07-07 00:00:00'));

create table pstudent_table_07
(
    s_date TIMESTAMP,
    s_name varchar not null,
    c_date TIMESTAMP,
    t_date TIMESTAMP,
    foreign key(c_date) references pclass_table_07(c_date)
) with (orientation=column) partition by range(s_date)  (
  partition part1 values less than ('1990-07-07 00:00:00'));


--删除外键表
drop table pclass_table_07 cascade;
drop table pteacher_table_07 cascade;
drop table pstudent_table_07 cascade;