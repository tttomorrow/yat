-- @testpoint: 创建行存分区表，设定分区字段为“char”
-- @modified at: 2020-11-16

drop table if exists special_char_09;
CREATE TABLE special_char_09 (c1 "char",c2 int) WITH (orientation=row, compression=no)
PARTITION BY RANGE (c1)
(
        PARTITION P1 VALUES LESS THAN('g'),
        PARTITION P2 VALUES LESS THAN('n'),
        PARTITION P3 VALUES LESS THAN('t'),
        PARTITION P4 VALUES LESS THAN('z'));

insert into special_char_09 values ('m',1);
select * from special_char_09;
drop table special_char_09;