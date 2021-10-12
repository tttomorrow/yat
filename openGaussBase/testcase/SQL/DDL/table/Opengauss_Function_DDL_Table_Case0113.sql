-- @testpoint: 创建列类型是任意精度型-DECIMAL[(p[,s])]的表

drop table if exists decimal_type_t1;
CREATE TABLE decimal_type_t1
(
    DT DECIMAL(10,4)
);
INSERT INTO decimal_type_t1 VALUES(123456.122331);

select * from decimal_type_t1;
drop table if exists decimal_type_t1;