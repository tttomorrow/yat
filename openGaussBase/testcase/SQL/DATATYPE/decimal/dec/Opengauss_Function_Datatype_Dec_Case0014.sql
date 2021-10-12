-- @testpoint: 创建列存分区表，精度在合理范围值内，插入值
-- @modified at: 2020-11-23

drop table if exists dec_14;
create table dec_14 (c1 dec(4,2),c2 int) with (orientation=column, compression=no)
PARTITION BY RANGE (c1)
(
        PARTITION P1 VALUES LESS THAN(10),
        PARTITION P2 VALUES LESS THAN(20),
        PARTITION P3 VALUES LESS THAN(30),
        PARTITION P4 VALUES LESS THAN(40),
        PARTITION P5 VALUES LESS THAN(50),
        PARTITION P6 VALUES LESS THAN(60),
        PARTITION P7 VALUES LESS THAN(MAXVALUE)
);
insert into dec_14 values (11.11,1);
select * from dec_14;
drop table dec_14;