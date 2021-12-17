-- @testpoint: pg_tablespace_size(name)函数的异常校验，合理报错

select pg_tablespace_size(9877653246990983456789);

select pg_tablespace_size();

select pg_tablespace_size('ds_location33','ds_location33','ds_location33');
