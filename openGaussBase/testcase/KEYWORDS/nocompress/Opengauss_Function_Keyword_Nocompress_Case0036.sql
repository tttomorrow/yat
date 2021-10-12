-- @testpoint: opengauss关键字nocompress(非保留)，建表时不指定压缩模式

create table if not exists table_828_1(ind int) nocompress;
select relcmprs from PG_CLASS where relname = 'table_828_1';
drop table if exists table_828_1 cascade;


