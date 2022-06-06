-- @testpoint: PostGIS功能覆盖，查询判断geogA与geogB边缘是否接触,ST_Touches

--step1:创建表   expect:成功
drop table if exists t_postgis_0016_01;
drop table if exists t_postgis_0016_02;
drop table if exists t_postgis_0016_03;
create table t_postgis_0016_01 (smgeometry geometry(Point,4490));
create table t_postgis_0016_02 (smgeometry geometry(MultiLineString,4490));
create table t_postgis_0016_03 (smgeometry geometry(MultiPolygon,4490));

--step2:插入数据   expect:成功
insert into t_postgis_0016_01 values(ST_GeomFromText('Point(2 1)',4490));
insert into t_postgis_0016_01 values(ST_GeomFromText('Point(5 9)',4490));

insert into t_postgis_0016_02 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(2 1,3 2,5 4))',4490));
insert into t_postgis_0016_02 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(1 1,2 0,3 1))',4490));
insert into t_postgis_0016_02 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(1 2,2 1,3 1))',4490));

insert into t_postgis_0016_03 values(ST_GeomFromText('MultiPolygon(((1 0, 0 1, 1 2, 2 1, 1 0), (2 0, 1 1, 2 2, 3 1, 2 0)))',4490));
insert into t_postgis_0016_03 values(ST_GeomFromText('MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))',4490));
insert into t_postgis_0016_03 values(ST_GeomFromText('MULTIPOLYGON (((2 0, 3 1, 2 2, 1.5 1.5, 2 1, 1.5 0.5, 2 0)), ((1 0, 1.5 0.5, 1 1, 1.5 1.5, 1 2, 0 1, 1 0)))',4490));

--step3:查看数据   expect:成功
--判断点线边缘是否接触
select ST_Touches(t1.smgeometry,t2.smgeometry) from t_postgis_0016_01 t1,t_postgis_0016_02 t2;
--判断点面边缘是否接触
select ST_Touches(t1.smgeometry,t3.smgeometry) from t_postgis_0016_01 t1,t_postgis_0016_03 t3;
--判断线面边缘是否接触
select ST_Touches(t2.smgeometry,t3.smgeometry) from t_postgis_0016_02 t2,t_postgis_0016_03 t3;

--step4:清理环境   expect:成功
drop table t_postgis_0016_01 cascade;
drop table t_postgis_0016_02 cascade;
drop table t_postgis_0016_03 cascade;

