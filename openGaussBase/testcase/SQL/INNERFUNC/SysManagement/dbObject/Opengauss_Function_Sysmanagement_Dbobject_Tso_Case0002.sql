-- @testpoint: pg_tablespace_size(oid)函数的异常校验，合理报错


select pg_tablespace_size();
select pg_tablespace_size('*&^%$$%^^&');
select pg_tablespace_size(a.oid,a.oid,a.oid) from PG_TABLESPACE a where a.spcname='ds_location333';