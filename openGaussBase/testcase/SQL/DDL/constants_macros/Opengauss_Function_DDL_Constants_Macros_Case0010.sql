--  @testpoint:null值作为对象名使用
--null作为表名,合理报错
drop table if exists null;
create table null(id int);
--null作为列名,合理报错
drop table if exists test1;
create table test1(null int);
--null作为数据类型，合理报错
drop table if exists test1;
create table test1(id null);