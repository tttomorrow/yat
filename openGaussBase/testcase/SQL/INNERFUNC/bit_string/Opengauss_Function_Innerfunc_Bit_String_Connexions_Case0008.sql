-- @testpoint: 操作符||，bit和bit varying为null
DROP TABLE IF EXISTS bit_type_t1;
CREATE TABLE bit_type_t1(BT_COL1 BIT(3),BT_COL2 BIT VARYING(5)) ;
insert into bit_type_t1(BT_COL1) values (B'101');
SELECT BT_COL1 || BT_COL2 from bit_type_t1 AS RESULT;
DROP TABLE IF EXISTS bit_type_t1;