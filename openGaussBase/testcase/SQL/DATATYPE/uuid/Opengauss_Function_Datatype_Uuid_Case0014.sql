-- @testpoint: 创建列存分区表，合理报错

drop table if exists test_uuid_14;
create table test_uuid_14 (c1 uuid,c2 int) with(orientation=column)
PARTITION BY RANGE (c1)
(
        PARTITION P4 VALUES LESS THAN('zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz'),
        PARTITION P5 VALUES LESS THAN(MAXVALUE)
);