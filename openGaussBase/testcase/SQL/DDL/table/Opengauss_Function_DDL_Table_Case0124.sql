-- @testpoint: 创建列为浮点类型的表，精度p超过1000或s非正整数时合理报错
drop table if exists table_1;
drop table if exists table_2;
drop table if exists table_3;
drop table if exists table_4;
drop table if exists table_5;
drop table if exists table_6;
drop table if exists table_7;
drop table if exists table_8;
create table table_2(a integer(1,1));
create table table_3(a integer(1,0));
create table table_4(a integer(500,200));
create table table_5(a integer(1000,0));
create table table_6(a integer(1000,100));
create table table_7(a integer(1000,1000));
--ERROR:  NUMERIC precision 1001 must be between 1 and 1000
create table table_8(a integer(1001,1000));
--ERROR:  invalid input syntax for integer: "0.5"
create table table_1(a integer(1,0.5));
drop table if exists table_2;
drop table if exists table_1;
drop table if exists table_3;
drop table if exists table_4;
drop table if exists table_5;
drop table if exists table_6;
drop table if exists table_7;
drop table if exists table_8;