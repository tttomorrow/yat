-- @testpoint: 创建列类型是位串类型的表
drop table if exists bit_type_t1;
CREATE TABLE bit_type_t1(BT_COL1 INTEGER,BT_COL2 BIT(3),BT_COL3 BIT VARYING(5));
insert into bit_type_t1 values(122,'100'::bit(3),'10001');
--select * from bit_type_t1;
drop table if exists bit_type_t1;


drop table if exists bit_type_t2;
CREATE TABLE bit_type_t2(BT_COL1 INTEGER,BT_COL2 BIT,BT_COL3 BIT VARYING) ;
insert into bit_type_t2 values(122,'1','10001');
select * from bit_type_t2;
drop table if exists bit_type_t1;
drop table if exists bit_type_t2;


