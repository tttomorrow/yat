-- @testpoint: 创建列类型是JSON类型的表
drop table if exists table_2;
create table table_2(a json);
insert into table_2 values('{"col1":1,"col2":"francs","col3":"male"}');
insert into table_2 values('{"col1":2,"col2":"fp","col3":"female"}');
select * from table_2;
drop table if exists table_2;
