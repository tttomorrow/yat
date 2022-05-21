-- @testpoint: 验证geometry(MultiPolygon)类型的应用

--step1:创建表和函数   expect:成功
drop table if exists t_postgis_0009;
drop function if exists uuid_generate_v4() cascade;

create or replace function uuid_generate_v4()
returns uuid
as
'select md5(random()::text || clock_timestamp()::text)::uuid;'
language sql;
/

create table t_postgis_0009 (
    smuserid integer default 0 not null,
    smarea double precision default 0 not null,
    smperimeter double precision default 0 not null,
    smgeometry geometry(multipolygon,4490),
    field_smuserid integer default 0,
    prov integer,
    name character varying(5000),
    code character varying(5000),
    sjly_code character varying(5000),
    sjly_name character varying(5000),
    level_user character varying(5000),
    ad_code character varying(5000),
    p_key uuid default uuid_generate_v4() not null);

--step2:插入数据   expect:成功
--边界由两个外环和一个内环组成(相离)
insert into t_postgis_0009 values(default,default,default,ST_GeomFromText('MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))',4490),

--边界由两个外环组成（相切）
insert into t_postgis_0009 values(default,default,default,ST_GeomFromText('MULTIPOLYGON (((2 0, 3 1, 2 2, 1.5 1.5, 2 1, 1.5 0.5, 2 0)), ((1 0, 1.5 0.5, 1 1, 1.5 1.5, 1 2, 0 1, 1 0)))',4490),

--边界重叠(相交)
insert into t_postgis_0009 values(default,default,default,ST_GeomFromText('MULTIPOLYGON (((1 0, 0 1, 1 2, 2 1, 1 0), (2 0, 1 1, 2 2, 3 1, 2 0)))',4490),

--插入geometry类型的数据
insert into t_postgis_0009 values(1,default,default,

--step3:查看multipolygon类型所在字段数据   expect:成功
select smgeometry from t_postgis_0009;
--查看多边形的ewkt表示形式
select st_asewkt(smgeometry) from t_postgis_0009 where smuserid=1;

--step4:清理环境   expect:成功
drop table t_postgis_0009;
