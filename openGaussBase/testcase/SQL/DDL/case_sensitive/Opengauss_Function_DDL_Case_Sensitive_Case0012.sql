--  @testpoint: 子查询验证字段名大小写
select * from false_1 where b in (select b from wms);
select * from false_1 where B in (select b from wms);
select * from false_1 where b in (select B from wms);
select * from false_1 where b in (select B from WMS);