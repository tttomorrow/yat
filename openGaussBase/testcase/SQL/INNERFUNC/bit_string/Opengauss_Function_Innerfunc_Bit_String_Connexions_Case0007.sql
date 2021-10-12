-- @testpoint: 操作符||，bit少参，合理报错
DROP TABLE IF EXISTS bit_type_t1;
CREATE TABLE bit_type_t1(BT_COL1 BIT(3),BT_COL2 BIT VARYING(5)) ;
insert into bit_type_t1 values (B'101', B'00');
SELECT BT_COL1 || from bit_type_t1 AS RESULT;
DROP TABLE IF EXISTS bit_type_t1;