--  @testpoint:列名出现关键字as；as大小写混合，应该报错
drop table if exists test_as_001 ;
create table test_as_001 (as int);