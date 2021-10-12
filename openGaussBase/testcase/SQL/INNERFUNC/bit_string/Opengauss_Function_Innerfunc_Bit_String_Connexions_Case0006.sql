-- @testpoint: 操作符||，bit(n)、bit varying(n)与整型/字符型，合理报错
DROP TABLE IF EXISTS bit_type_t1;
CREATE TABLE bit_type_t1(BT_COL1 BIT(3),BT_COL2 int) ;
insert into bit_type_t1 values (B'111', 11);
SELECT BT_COL1|| BT_COL2 from bit_type_t1 AS RESULT;
SELECT BT_COL1|| 'aa' from bit_type_t1 AS RESULT;
DROP TABLE IF EXISTS bit_type_t1;