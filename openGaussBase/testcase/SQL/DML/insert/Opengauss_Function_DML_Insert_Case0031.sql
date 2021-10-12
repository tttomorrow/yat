-- @testpoint: 插入数据，数据类型不符，合理报错
--建表
drop table if exists COMPANY;
CREATE TABLE COMPANY(
   ID INT PRIMARY KEY     NOT NULL,
   NAME           TEXT    NOT NULL,
   AGE            INT     NOT NULL,
   ADDRESS        CHAR(50),
   SALARY         REAL,
   JOIN_DATE      DATE
);
--省略列名，插入数据，类型不符，报错
insert into COMPANY values('hello','lisq',28);
--删表
drop table COMPANY;