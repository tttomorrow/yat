-- @testpoint: 操作符||，bit(n)、bit varying(n)补齐用法
DROP TABLE IF EXISTS bit_type_t1;
CREATE TABLE bit_type_t1(BT_COL1 BIT(3),BT_COL2 BIT VARYING(5)) ;
insert into bit_type_t1 values (B'111', B'11');
SELECT BT_COL1 ::bit(5) || BT_COL2 ::bit varying(6) from bit_type_t1 AS RESULT;
DROP TABLE IF EXISTS bit_type_t1;