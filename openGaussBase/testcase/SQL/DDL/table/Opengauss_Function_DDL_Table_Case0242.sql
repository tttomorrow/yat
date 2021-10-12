-- @testpoint: 创建临时表使用表结构里的列，别名可加可省略
drop table if exists ct_as;
drop table if exists ct_tbl_as;
create table ct_tbl_as(
        c_id int, c_int int, c_integer integer,
        c_real real, c_decimal decimal(38),  c_numeric numeric(38),
        c_char char(50) not null, c_varchar varchar(20), c_varchar2 varchar2(4000)

)
PARTITION BY RANGE (c_integer)
(
);
insert into ct_tbl_as  values(1,12,-2,123.63,563.893,852.33,'qwe','ugfd','weewvbgfyui');
insert into ct_tbl_as  values(2,22,8,123.63,563.893,852.33,'qedc','kjjhbn','rtygftyui');
insert into ct_tbl_as  values(3,32,12,123.63,563.893,852.33,'qhfs','ihgd','wertrtgui');
create temporary table ct_as as select c_char c_u,c_varchar2 from ct_tbl_as;
select * from ct_as order by ct_as desc;
insert into ct_as(c_u,c_varchar2) values(31, 1000);
drop table if exists ct_as;
drop table if exists ct_tbl_as;