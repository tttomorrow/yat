-- @testpoint: 测试列名长度最大支持63字节

drop table if exists table_1;
create table table_1(qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq int);
insert into table_1 values(1);
insert into table_1 values(2);
insert into table_1 values(3);
select * from table_1;
drop table if exists table_1;