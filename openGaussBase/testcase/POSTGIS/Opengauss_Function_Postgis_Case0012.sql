-- @testpoint: 验证geometry(MultiLineString)类型的应用

--step1:创建表   expect:成功
drop table if exists t_postgis_0011;
create table t_postgis_0011 (
    smid integer not null,
    smuserid integer default 0 not null,
    smtopoerror integer default 0 not null,
    smlength double precision default 0 not null,
    smgeometry geometry(multilinestring,4490),
    t integer,
    name character varying(5000),
    obj_code character varying(5000),
    obj_name character varying(5000),
    center_x double precision,
    center_y double precision,
    cros_boun_type character varying(5000),
    rv_type character varying(5000),
    rv_grad character varying(5000),
    rv_bas_area numeric(16,2),
    rv_len numeric(12,3),
    element_type character varying(5000) default null::character varying);

--step2:插入数据   expect:成功
--边界是两个LineString元素的四个端点
insert into t_postgis_0011 values(99205,default,default,default,ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(2 3,3 2,5 4))',4490),0,'幸福沟','KF383C00000H','东泉河','90.65097593450778','33.93363516512833','5','1','2',43.000, 336.00,default);

--边界是两个不重叠的端点
insert into t_postgis_0011 values(99205,default,default,default,ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(1 2,2 1,3 1))',4490),0,'幸福沟','KF383C00000H','东泉河','90.65097593450778','33.93363516512833','5','1','2',43.000, 336.00,default);

--其中一个LineString元素的内部出现了相交，边界是四个端点
insert into t_postgis_0011 values(99205,default,default,default,ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(1 1,2 0,3 1))',4490),0,'幸福沟','KF383C00000H','东泉河','90.65097593450778','33.93363516512833','5','1','2',43.000, 336.00,default);

--非闭合，边界是四个端点
insert into t_postgis_0011 values(99205,default,default,default,ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(0 2,1 1,2 0))',4490),0,'幸福沟','KF383C00000H','东泉河','90.65097593450778','33.93363516512833','5','1','2',43.000, 336.00,default);

--非闭合
insert into t_postgis_0011 values(99205,default,default,default,ST_GeomFromText('MultiLineString((0 0,1 1,1 2,0 3),(0 3,-1 2,-1 1,0 0))',4490),0,'幸福沟','KF383C00000H','东泉河','90.65097593450778','33.93363516512833','5','1','2',43.000, 336.00,default);

--闭合
insert into t_postgis_0011 values(99205,default,default,default,ST_GeomFromText('MultiLineString((0 0,0 1,1 1,1 0,0 0),(2 2,3 2,3 3,2 3,2 2))',4490),0,'幸福沟','KF383C00000H','东泉河','90.65097593450778','33.93363516512833','5','1','2',43.000, 336.00,default);

--插入geometry类型的数据
insert into t_postgis_0011 values(99208,default,default,default,

--step3:查看数据   expect:成功
select smgeometry from t_postgis_0011;
select st_asewkt(smgeometry) from t_postgis_0011 where smid=99208;
select st_astext(smgeometry) from t_postgis_0011 where smid=99208;

--step4:清理环境   expect:成功
drop table t_postgis_0011 cascade;

