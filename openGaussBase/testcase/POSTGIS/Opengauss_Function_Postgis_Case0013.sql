-- @testpoint: PostGIS功能覆盖，获取对象中心点ST_Centroid

--step1:创建表   expect:成功
drop table if exists t_postgis_0012;
create table t_postgis_0012 (
    smid integer not null,
    smgeometry1 geometry(point),
    smgeometry2 geometry(multilinestring,4490),
    smgeometry3 geometry(multipolygon,4490));

--step2:插入数据(点，线，面)   expect:成功
insert into t_postgis_0012 values(99001,
ST_GeomFromText('Point(0 0)'),
ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(2 3,3 2,5 4))',4490),
ST_GeomFromText('MultiPolygon(((1 0, 0 1, 1 2, 2 1, 1 0), (2 0, 1 1, 2 2, 3 1, 2 0)))',4490));

insert into t_postgis_0012 values(99002,
ST_GeomFromText('Point(1 2)'),
ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(1 1,2 0,3 1))',4490),
ST_GeomFromText('MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))',4490));

insert into t_postgis_0012 values(99002,
ST_GeomFromText('Point(3 4)'),
ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(1 2,2 1,3 1))',4490),
ST_GeomFromText('MULTIPOLYGON (((2 0, 3 1, 2 2, 1.5 1.5, 2 1, 1.5 0.5, 2 0)), ((1 0, 1.5 0.5, 1 1, 1.5 1.5, 1 2, 0 1, 1 0)))',4490));

--step3:查看数据   expect:成功
--获取点的中心点
select smgeometry1 from t_postgis_0012;
select st_asewkt(st_centroid(smgeometry1)) from t_postgis_0012;

--获取线的中心点
select smgeometry2 from t_postgis_0012;
select st_asewkt(st_centroid(smgeometry2)) from t_postgis_0012;

--获取面的中心点
select smgeometry3 from t_postgis_0012;
select st_asewkt(st_centroid(smgeometry3)) from t_postgis_0012;

--step4:清理环境   expect:成功
drop table t_postgis_0012 cascade;
