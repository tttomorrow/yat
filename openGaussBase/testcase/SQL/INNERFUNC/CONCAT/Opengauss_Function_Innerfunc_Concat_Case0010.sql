-- @testpoint:join条件
create table zsharding_tbl(c_id int, c_int int, c_integer integer);
select distinct B.c_id CID,B.c_int CINT,B.c_integer INTER from zsharding_tbl a join zsharding_tbl b on concat(B.c_id,B.c_int)='34';
drop table zsharding_tbl;
