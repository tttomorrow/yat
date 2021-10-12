-- @testpoint: 创建列类型是位串类型的表，插入数据范围超过指定长度时合理报错
drop table if exists bit_type_t3;
CREATE TABLE bit_type_t3(BT_COL1 INTEGER,BT_COL2 BIT(3),BT_COL3 BIT VARYING(5)) ;
insert into bit_type_t3 values(122,'10001','1000');
select * from bit_type_t3;
drop table if exists bit_type_t3;

drop table if exists bit_type_t4;
CREATE TABLE bit_type_t4(BT_COL1 INTEGER,BT_COL2 BIT(3),BT_COL3 BIT VARYING(5)) ;
insert into bit_type_t4 values(122,'101','101010');
select * from bit_type_t4;
drop table if exists bit_type_t4;