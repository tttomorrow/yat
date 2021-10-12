-- @testpoint: 创建列存分区表，字段类型为“char”


drop table if exists special_char_12;
CREATE TABLE special_char_12 (c1 "char",c2 int) WITH (orientation=COLUMN, compression=no)
PARTITION BY RANGE (c1)
(
        PARTITION P1 VALUES LESS THAN('g'),
        PARTITION P2 VALUES LESS THAN('n'),
        PARTITION P3 VALUES LESS THAN('t'),
        PARTITION P4 VALUES LESS THAN('z'));
        
insert into special_char_12 values ('1',1);
select * from special_char_12;
drop table if exists special_char_12;