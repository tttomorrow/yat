-- @testpoint: to_clob函数入参给rowid，rownum，在入参是rowid时合理报错

select count(to_clob(rowid));
select count(to_clob(rownum));