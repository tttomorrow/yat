-- @testpoint: 创建一个包含所有数值类型的表
drop table if exists table_1;
create table table_1(a TINYINT,b SMALLINT,c INTEGER,d BINARY_INTEGER,
e BIGINT,f NUMERIC(5,4),g DECIMAL(10,3),h NUMBER(5,2),i SMALLSERIAL,
j SERIAL,k BIGSERIAL,l REAL,m DOUBLE PRECISION,n FLOAT(25),o BINARY_DOUBLE,p DEC(10,2),q INTEGER(6,3)
);
insert into table_1 values(123,456,852,7895,85,5.1234,935855.9638552,852.963,7896,1236,852,7865,852,741,7925.246,8822,123.123);
select * from table_1;
drop table if exists table_1;
