-- @testpoint: 创建列存分区表，合理报错

drop table if exists test_uuid_14;
create table test_uuid_14 (c1 uuid,c2 int) with(orientation=column)
PARTITION BY RANGE (c1)
(
        PARTITION P1 VALUES LESS THAN('11111111-1111-1111-1111-111111111111'),
        PARTITION P2 VALUES LESS THAN('22222222-2222-2222-2222-222222222222'),
        PARTITION P3 VALUES LESS THAN('33333333-3333-3333-3333-333333333333'),
        PARTITION P4 VALUES LESS THAN('zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz'),
        PARTITION P5 VALUES LESS THAN(MAXVALUE)
);