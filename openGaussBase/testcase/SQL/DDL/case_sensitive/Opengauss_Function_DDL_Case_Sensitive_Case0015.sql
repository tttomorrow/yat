--  @testpoint: --WITH语句验证临时表名大小写
with
cf as (select * from wms)
select * from CF;
with
cf as (select * from wms),
cd as (select * from CF)
select * from cd;
