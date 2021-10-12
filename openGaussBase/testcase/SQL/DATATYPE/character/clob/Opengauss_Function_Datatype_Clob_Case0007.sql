-- @testpoint: 建表作为数据类型：列存global临时表，合理报错
drop table if exists test_clob_07 CASCADE;
create global TEMPORARY table test_clob_07(name clob) with (orientation=column);
