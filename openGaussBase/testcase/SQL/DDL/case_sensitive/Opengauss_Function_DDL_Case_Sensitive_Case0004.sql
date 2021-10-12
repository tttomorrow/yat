--  @testpoint: --insert验证字段大小写
drop table if EXISTS false_1 CASCADE;
create table false_1(A int,b CHAR(10));

insert into false_1(a) values(3);
insert into false_1(A) values(5);
insert into false_1(b) values('xx'),('wms');
insert into false_1(B) values('xx');
select * from false_1;