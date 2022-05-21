-- @testpoint: 验证integer,varchar,smallint,double decision,bytea,date,boolean类型(不合理)的应用，合理报错

--step1:创建表   expect:成功
drop table if exists t_postgis_0006 cascade;
create table t_postgis_0006 (
    smdatasetid integer not null,
    smdatasetname character varying(5000) not null,
    smtablename character varying(5000) not null,
    smdatasettype smallint not null,
    smoption integer,
    smenctype integer default 0 not null,
    smpixelformat integer default 0 not null,
    smwidth integer,
    smheight integer,
    smeblocksize integer,
    smminz double precision default 0,
    smmaxz double precision default 0,
    smcolorspace integer default 0,
    smpyramid character varying(5000),
    smpyramidlevel integer default 0 not null,
    smblocksizes integer,
    smpalette bytea,
    smgeoleft double precision,
    smgeotop double precision,
    smgeoright double precision,
    smgeobottom double precision,
    smclipregion bytea,
    smlastupdatetime date default current_date,
    smcreator character varying(5000),
    smnovalue double precision default '-9999'::integer,
    smextinfo character varying(2048),
    smstatisticsinfo text,
    smdescription character varying(5000),
    smschema character varying(5000) default 'public'::character varying,
    smiswkb boolean default false,
    smprojectinfo bytea);


--step2:插入不合理数据   expect:失败，合理报错
insert into t_postgis_0006 values(2147483648,'name1','name2',32767,1,2,3,4,5,6,321.321,321.321,7,'varying',8,9,E'\\xDEADBEEF',12.12,23.23,34.34,45.45,E'\\xABCD',date '08-25-2020','varying',21.21,'info','info:text','description','smschema',true,E'\\xABCDEF');

insert into t_postgis_0006 values(1,to_char(lpad('a',5001,'x')),to_char(lpad('b',5000,'y')),32767,1,default,default,4,5,6,default,default,default,to_char(lpad('c',5000,'z')),default,9,E'\\xDEADBE',121.121,232.232,343.343,454.454,E'\\xABCD',default,to_char(lpad('d',5000,'q')),default,to_char(lpad('d',2048,'g')),'info:text','description',default,default,E'\\xABCDEF');

insert into t_postgis_0006 values(1,'name1','name2',NULL,1,2,3,4,5,6,321.321,321.321,7,'varying',8,9,E'\\xDEADBEEF',12.12,23.23,34.34,45.45,E'\\xABCD',date '08-25-2020','varying',21.21,'info','info:text','description','smschema',true,E'\\xABCDEF');

insert into t_postgis_0006 values(1,'name1','name2',NULL,1,2,3,4,5,6,321.321,321.321,7,'varying',8,9,E'\\xDEADBEEF',12.12,23.23,34.34,45.45,E'\\xABCDE',date '08-25-2020','varying',21.21,'info','info:text','description','smschema',true,E'\\xABCDEF');

insert into t_postgis_0006 values(1,'name1','name2',NULL,1,2,3,4,5,6,321.321,321.321,7,'varying',8,9,E'\\xDEADBEEF',12.12,23.23,34.34,45.45,E'\\xABCDEF',date '08-25-2020','varying',21.21,to_char(lpad('d',2049,'g')),'info:text','description','smschema',true,E'\\xABCDEF');

--step3:查看数据   expect:数据为空
select * from t_postgis_0006;

--step4:清理环境   expect:成功
drop table t_postgis_0006;
