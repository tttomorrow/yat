-- @testpoint: 测试rownum是否为关键字，合理报错

--测试点1：验证行存表、列存表是否支持以rownum为表名
drop table if exists rownum;
create table rownum
(
    id int primary key,
    name varchar(10) not null
);
drop table if exists rownum;
create table rownum
(
    id int,
    name varchar(10) not null
) with (orientation = column);
drop table if exists rownum;
--测试点2：以rownum为列名
drop table if exists student;
create table student
(
    id int primary key,
    rownum varchar
);
--测试点3：以rownum为别名
select 2 rownum from dual;
--测试点4：以rownum为视图名
create view rownum as select * from pg_tablespace where spcname = 'pg_default';
--测试点5：以rownum为存储过程名
create or replace procedure rownum(id in int, name in varchar(10))
IS
BEGIN
insert into student values (id, name);
END;
/
call rownum(1, 'aaa');
drop table if exists student;
drop procedure if exists rownum;
