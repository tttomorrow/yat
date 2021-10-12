-- @testpoint: 操作符||，拆分用法
DROP TABLE IF EXISTS bit_type_t1;
CREATE TABLE bit_type_t1(BT_COL1 BIT(3),BT_COL2 BIT VARYING(5),BT_COL3 BIT(3)) ;
insert into bit_type_t1 values (B'101', B'00',B'101');
SELECT BT_COL1 || (BT_COL2 || BT_COL3) from bit_type_t1 AS RESULT;
DROP TABLE IF EXISTS bit_type_t1;