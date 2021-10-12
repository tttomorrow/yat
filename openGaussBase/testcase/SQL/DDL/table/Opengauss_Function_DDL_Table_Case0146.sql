-- @testpoint: 创建列类型包含多种几何类型的表
drop table if exists table_1;
create table table_1(a point,b lseg,c box,d path ,e circle);
insert into table_1 values('(2,3)','((1,1),(1,3))','((1,1),(3,3))','((1,1),(1,3),(2,4),(3,3),(4,2),(3,1),(1,1))','((3,3),1)');
select * from table_1;
drop table if exists table_1;
