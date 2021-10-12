-- @testpoint: 检测是否支持表中建立、更新、删除外键 行存 列存 内存表:success

drop table if exists pstudent_table_01 cascade;
drop table if exists pclass_table_01 cascade;
drop table if exists pteacher_table_01 cascade;

create table pclass_table_01
(
    c_date TIMESTAMP primary key,
    c_name varchar not null
)partition by range(c_date) interval ('10 day') (
  partition part1 values less than ('1990-01-01 00:00:00'));


create table pteacher_table_01
(
    t_date TIMESTAMP primary key,
    t_name varchar not null
)partition by range(t_date) interval ('10 day') (
  partition part1 values less than ('1990-01-01 00:00:00'));

create table pstudent_table_01
(
    s_date TIMESTAMP primary key,
    s_name varchar not null,
    c_date TIMESTAMP,
    t_date TIMESTAMP,
    foreign key(c_date) references pclass_table_01(c_date)
)partition by range(s_date) interval ('10 day') (
  partition part1 values less than ('1990-01-01 00:00:00'));

--外键的更新
alter table pstudent_table_01 add constraint fk_student_tid foreign key (t_date) references pteacher_table_01(t_date);

--外键的删除
alter table pstudent_table_01 drop constraint fk_student_tid;
alter table pstudent_table_01 drop constraint pstudent_table_01_c_date_fkey;

--删除外键表
drop table pclass_table_01 cascade;
drop table pteacher_table_01 cascade;
drop table if exists pstudent_table_01 cascade;
drop table if exists pclass_table_01 cascade;
drop table if exists pteacher_table_01 cascade;