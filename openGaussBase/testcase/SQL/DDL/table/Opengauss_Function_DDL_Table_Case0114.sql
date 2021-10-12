-- @testpoint: 创建列类型是NUMERIC[(p[,s])的表
drop table if exists NUMERIC_t1;
CREATE TABLE NUMERIC_t1
(
    DT DECIMAL(10,4)
);
INSERT INTO NUMERIC_t1 VALUES(123456.122331);

select * from  NUMERIC_t1;
drop table if exists NUMERIC_t1;