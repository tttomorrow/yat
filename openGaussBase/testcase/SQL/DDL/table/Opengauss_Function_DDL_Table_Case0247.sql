-- @testpoint: 与视图结合,先用查询视图，创建成功后，应该不带not null约束
drop view if exists ct_tbl_as_v;
drop table if exists ct_as;
drop table if exists ct_tbl_as;
create table ct_tbl_as(
        c_id int, c_int int, c_integer integer,
        c_real real, c_decimal decimal(38),  c_numeric numeric(38),
        c_char char(50) not null, c_varchar varchar(20), c_varchar2 varchar2(4000)

)
PARTITION BY RANGE (c_integer)
(
        partition P_20180121 values less than (0),
        partition P_20190122 values less than (10),
        partition P_20200123 values less than (20)
);
insert into ct_tbl_as  values(1,12,-2,123.63,563.893,852.33,'qwe','ugfd','weewvbgfyui');
insert into ct_tbl_as  values(2,22,8,123.63,563.893,852.33,'qedc','kjjhbn','rtygftyui');
insert into ct_tbl_as  values(3,32,12,123.63,563.893,852.33,'qhfs','ihgd','wertrtgui');
create view ct_tbl_as_v as (select c_char c1,c_varchar2 c2 from ct_tbl_as) union all (select c_char c3,c_varchar2 c4 from ct_tbl_as);
create table ct_as as select * from ct_tbl_as_v union all (select c_char c3,c_varchar2 c4 from ct_tbl_as);

select * from ct_tbl_as_v;
drop view if exists ct_tbl_as_v;
select * from ct_as order by ct_as desc;
drop table if exists ct_as;
drop table if exists ct_tbl_as;