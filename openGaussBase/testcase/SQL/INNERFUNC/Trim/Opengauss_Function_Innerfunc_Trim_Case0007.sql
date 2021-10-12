-- @testpoint: 字符处理函数trim，函数作为join条件项

drop table if exists zsharding_tbl;
create table zsharding_tbl(c_id int, c_int int, c_integer integer);
select distinct B.c_id CID,B.c_int CINT,B.c_integer INTER from zsharding_tbl a join zsharding_tbl b on trim('2' from '2342')='34';
drop table if exists zsharding_tbl;
