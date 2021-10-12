--  @testpoint: --创建普通约束区别大小写
drop table if exists false_2;
create table false_2(a int,b int);
alter table false_2 add constraint WMS check(B<100);
alter table false_2 add constraint WMS check(b<100);
alter table false_2 add constraint zz check(a<100);
alter table false_2 add constraint ZZ check(A<100);
SELECT conname,contype,condeferrable,condeferred,convalidated FROM PG_CONSTRAINT WHERE conname in ('wms','zz') order by conname;
SELECT conname,contype,condeferrable,condeferred,convalidated FROM PG_CONSTRAINT WHERE conname in ('WMS','ZZ') order by conname;
SELECT conname,contype,condeferrable,condeferred,convalidated FROM PG_CONSTRAINT WHERE conname='WMS';
SELECT conname,contype,condeferrable,condeferred,convalidated FROM PG_CONSTRAINT WHERE conname='wms';

alter table false_2 drop constraint wms;
alter table false_2 drop constraint WMS;
alter table false_2 drop constraint zz;
alter table false_2 drop constraint ZZ;

SELECT conname,contype,condeferrable,condeferred,convalidated FROM PG_CONSTRAINT WHERE conname in ('wms','zz') order by conname;
SELECT conname,contype,condeferrable,condeferred,convalidated FROM PG_CONSTRAINT WHERE conname in ('WMS','ZZ') order by conname;

drop table if exists false_2;
