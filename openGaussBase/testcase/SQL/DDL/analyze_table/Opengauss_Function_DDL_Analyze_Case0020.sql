-- @testpoint: analyze含有目前支持所有数据类型的表
drop table if exists tbl_008;
create table tbl_008
(
                col_tinyint                  tinyint,
                col_smallint         smallint,
                col_int                      integer,
                col_binary_int       binary_integer,
                col_bigint                   bigint,
                col_money            varchar(30),
                col_numeric                  numeric,
				col_number           number,
                col_smallserial      varchar(30),
				col_float            float(3),
				col_char                     char(30),
				col_boolean                      boolean
);
insert into tbl_008 values(10,-1562,13,134,1234,'aa',456,789,'bb',3.1415926,'cc','true');
insert into tbl_008 values(100,9152,13,134,1234,'aa',456,789,'bb',3.1415926,'cc','true');
insert into tbl_008 values(0,102,13,134,1234,'aa',456,789,'bb',3.1415926,'cc','true');
insert into tbl_008 values(255,32712,13,134,1234,'aa',456,789,'bb',3.1415926,'cc','true');
analyze tbl_008;
drop table if exists tbl_008;