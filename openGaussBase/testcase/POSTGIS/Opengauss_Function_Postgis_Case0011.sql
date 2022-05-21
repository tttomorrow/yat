-- @testpoint: 验证geometry(Point)类型的应用

--step1:创建表   expect:成功
drop table if exists t_postgis_0010;
create table t_postgis_0010 (
    smuserid integer default 0 not null,
    smgeometry geometry(point),
    id character varying(5000),
    name character varying(5000),
    x double precision,
    y double precision,
    p_key uuid default uuid_generate_v4() not null);

--step2:插入数据   expect:成功
insert into t_postgis_0010 values(default,ST_GeomFromText('Point(0 0)'),'1001','幸福沟','90.65097593450778','33.93363516512833','d90ef9ad-26ea-4cb3-ad8e-2619d1621bce');
insert into t_postgis_0010 values(default,ST_GeomFromText('Point(0 0)',0),'1002','幸福沟','90.65097593450778','33.93363516512833','d90ef9ad-26ea-4cb3-ad8e-2619d1621bce');
--直接插入gemometry类型  point(1 2)
insert into t_postgis_0010 values(default,'0101000000000000000000F03F0000000000000040','1004','幸福沟','90.65097593450778','33.93363516512833','d90ef9ad-26ea-4cb3-ad8e-2619d1621bce');

--step3:查看geometry(point)字段所在数据   expect:成功
select smgeometry from t_postgis_0010;
select st_asewkt(smgeometry) from t_postgis_0010 where id = 1004;

--step4:清理环境   expect:成功
drop table t_postgis_0010;

