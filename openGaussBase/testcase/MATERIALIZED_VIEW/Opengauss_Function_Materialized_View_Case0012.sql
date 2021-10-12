-- @testpoint: 测试materialized关键字情况，合理报错

--关键字检查，pg中未将materialized作为关键字，openGauss与pg保持一致
--行存表
drop table if exists materialized;
create table materialized
(
    id int primary key,
    name varchar(10) not null
);
drop table materialized;
--列存表
drop table if exists materialized;
create table materialized
(
    id int,
    name varchar(10) not null
) with (orientation = column);
drop table materialized;
--临时表
drop table if exists materialized;
create global temporary table materialized
(
    id int primary key,
    name varchar(10) not null
) on commit delete rows;
drop table materialized;
--列名
drop table if exists student;
create table student
(
    id int primary key,
    materialized varchar(10) not null
);
drop table student;
--别名
select 2 materialized from sys_dummy;
select 2 as materialized from sys_dummy;
--视图名
drop view if exists materialized;
create view materialized as select * from pg_tablespace where spcname = 'pg_default';
drop view materialized;
drop materialized view if exists materialized;
create materialized view materialized as select * from pg_tablespace where spcname = 'pg_default';
drop materialized view materialized;