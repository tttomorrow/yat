--  @testpoint: --drop 验证表名大小写敏感
drop table if exists FALSE_1;
DROP TABLE if exists falsE_1;
select * from falsE_1;
select * from false_1;
drop table false_1;
drop table WMS;
drop table wms;