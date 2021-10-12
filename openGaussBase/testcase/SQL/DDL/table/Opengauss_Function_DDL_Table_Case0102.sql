-- @testpoint: 测试列名长度超过63字节，实际列名为前63字节
drop table if exists table_1;
create table table_1(qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq int);
insert into table_1 values(1);
insert into table_1 values(2);
insert into table_1 values(3);
select * from table_1;
drop table if exists table_1;
