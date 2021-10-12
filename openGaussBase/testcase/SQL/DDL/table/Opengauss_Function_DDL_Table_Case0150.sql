-- @testpoint: 创建列类型是位串类型的表
drop table if exists bit_type_t5;
CREATE TABLE bit_type_t5(BT_COL1 INTEGER,BT_COL2 BIT(3),BT_COL3 BIT VARYING(5)) ;
insert into bit_type_t5 values(122,'1110'::bit(3),'11111');
--select * from bit_type_t5;
insert into bit_type_t5 values(122,'11'::bit(3),'10101');
--select * from bit_type_t5;
drop table if exists bit_type_t5;

drop table if exists bit_type_t6;
CREATE TABLE bit_type_t6(BT_COL1 INTEGER,BT_COL2 BIT(3),BT_COL3 BIT VARYING(5)) ;
insert into bit_type_t6 values(122,'111','101101'::bit varying(5));
--select * from bit_type_t6;
insert into bit_type_t6 values(122,'111','101'::bit varying(5));
--select * from bit_type_t6;
drop table if exists bit_type_t6;


drop table if exists bit_type_t7;
CREATE TABLE bit_type_t7(BT_COL1 INTEGER,BT_COL2 BIT(3),BT_COL3 BIT VARYING(5)) ;
insert into bit_type_t7 values(122,'111','101101'::bit varying(4));
--select * from bit_type_t7;
insert into bit_type_t7 values(122,'111','10'::bit varying(7));
--select * from bit_type_t7;
drop table if exists bit_type_t7;