-- @testpoint: 创建列类型是NUMBER[(p[,s])的表
drop table if exists NUMBER_t1;
CREATE TABLE NUMBER_t1
(
    DT DECIMAL(12,3)
);
INSERT INTO NUMBER_t1 VALUES(14523456.1233);

select * from  NUMBER_t1;
drop table if exists NUMBER_t1;