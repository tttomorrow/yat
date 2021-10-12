-- @testpoint: 创建行存分区表，精度在合理范围值，插入数据
-- @modified at: 2020-11-23

drop table if exists dec_11;
CREATE TABLE dec_11 (c1 DEC(4,2),c2 int) WITH (orientation=row, compression=no)
PARTITION BY RANGE (c1)
(
        PARTITION P1 VALUES LESS THAN(10),
        PARTITION P2 VALUES LESS THAN(20),
        PARTITION P3 VALUES LESS THAN(30),
        PARTITION P4 VALUES LESS THAN(40),
        PARTITION P5 VALUES LESS THAN(50),
        PARTITION P6 VALUES LESS THAN(60),
        PARTITION P7 VALUES LESS THAN(MAXVALUE));
insert into dec_11 values (11.11,1);
select * from dec_11;
drop table dec_11;