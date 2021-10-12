-- @testpoint: 使用drop temporary语句删除普通表，合理报错
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_023;
create  table temp_table_023
(
  empno    varchar2(20) not null,
  empname  varchar2(20),
  job      varchar2(20),
  mgr      number(38),
  hiredate date,
  salary   number(38),
  deptno   number(38)
);
--插入数据
insert into temp_table_023 values('7369','smith','clerk','7902',to_date('1980-12-17','yyyy-mm-dd'),'800','20');
insert into temp_table_023 values('7499','allen','salesman','7698',to_date('1981-02-20','yyyy-mm-dd'),'1600','30');
insert into temp_table_023 values('7521','ward','salesman','7698',to_date('1981-02-22','yyyy-mm-dd'),'1250','30');
insert into temp_table_023 values('7566','jones','manager','7839',to_date('1981-04-02','yyyy-mm-dd'),'2975','20');
insert into temp_table_023 values('7654','martin','salesman','7698',to_date('1981-09-28','yyyy-mm-dd'),'1250','30');
insert into temp_table_023 values('7698','blake','manager','7839',to_date('1981-05-01','yyyy-mm-dd'),'2850','30');
--删表添加temporary，合理报错
drop temporary table if exists temp_table_023;
--删表
drop table temp_table_023;