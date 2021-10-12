-- @testpoint: 操作符||，没有长度的bit
DROP TABLE IF EXISTS bit_type_t1;
CREATE TABLE bit_type_t1(BT_COL1 BIT,BT_COL2 BIT VARYING) ;
insert into bit_type_t1 values (B'1', B'0111111');
SELECT BT_COL1 || BT_COL2 from bit_type_t1 AS RESULT;
DROP TABLE IF EXISTS bit_type_t1;