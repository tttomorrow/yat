-- @testpoint: 创建多种数值类型、货币类型、布尔类型的表
drop table if exists table_1;
create table table_1(a TINYINT,b SMALLINT,c INTEGER,d BINARY_INTEGER,e BIGINT,f money,g BOOLEAN);
insert into table_1 values(123,456,852,7895,85,2324.12,true);
drop table if exists table_1;


drop table if exists table_2;
create table table_2(f NUMERIC(5,4),g DECIMAL(10,3),h NUMBER(5,2),i SMALLSERIAL,j SERIAL,k BIGSERIAL,a money,b BOOLEAN);
insert into table_2 values(5.96,852.963,789.4561,1236,852,12324.123,7893,true);
drop table if exists table_2;

drop table if exists table_3;
create table table_3(l REAL,m DOUBLE PRECISION,n FLOAT(25),o BINARY_DOUBLE,p DEC(10,2),q INTEGER(6,3),a money,b BOOLEAN);
insert into table_3 values(7865,852,741,7925.246,8822,324.121243,797.123425,true);
select * from table_3;
drop table if exists table_3;