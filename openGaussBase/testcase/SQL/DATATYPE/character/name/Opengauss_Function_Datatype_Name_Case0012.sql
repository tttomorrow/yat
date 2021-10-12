-- @testpoint: 创建列存分区表，分区字段设为name,合理报错
-- @modified at: 2020-11-13


drop table if exists name_15;
--name类型不支持列存
CREATE TABLE name_15 (c1 name,c2 int)
WITH (orientation=COLUMN, compression=no)
PARTITION BY RANGE (c1)
(
        PARTITION P1 VALUES LESS THAN('g'),
        PARTITION P2 VALUES LESS THAN('n'),
        PARTITION P3 VALUES LESS THAN('q'),
        PARTITION P4 VALUES LESS THAN('t'),
        PARTITION P5 VALUES LESS THAN('z')
);
insert into name_15 values ('d',1);
select * from name_15;
drop table name_15;