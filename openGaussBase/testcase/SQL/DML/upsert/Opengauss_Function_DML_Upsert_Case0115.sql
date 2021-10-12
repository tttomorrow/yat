--  @testpoint:excluded保留关键字，作为表名，合理报错
 drop table if exists excluded;
--建表指定id为唯一约束，excluded作为表名合理报错
create table excluded
(
   name nvarchar2(20)  ,
   id serial unique  ,
   address nvarchar2(50)
) ;

