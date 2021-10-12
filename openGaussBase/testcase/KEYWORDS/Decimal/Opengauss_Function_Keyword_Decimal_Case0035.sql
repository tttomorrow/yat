--  @testpoint:定义数据类型是decimal，插入decimal数据查询
drop table if exists decimal_type_t1;
CREATE TABLE decimal_type_t1
(DT_COL1 DECIMAL(10,4)
);
INSERT INTO decimal_type_t1 VALUES(123456.122331);
SELECT * FROM decimal_type_t1;
DROP TABLE decimal_type_t1;