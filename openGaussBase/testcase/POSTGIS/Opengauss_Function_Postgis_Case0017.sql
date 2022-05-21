-- @testpoint: PostGIS功能覆盖，查询判断geogA与geogB是否重叠,ST_Overlaps

--step1:创建表   expect:成功
drop table if exists t_postgis_0017_01;
drop table if exists t_postgis_0017_02;

create table t_postgis_0017_01 (smgeometry1 geometry(MultiLineString,4490),
                              smgeometry2 geometry(MultiPolygon,4490),
                              smgeometry3 geometry(Point,4490));
create table t_postgis_0017_02 (smgeometry1 geometry(MultiLineString,4490),
                              smgeometry2 geometry(MultiPolygon,4490),
                              smgeometry3 geometry(Point,4490));

--step2:插入数据   expect:成功
insert into t_postgis_0017_01 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(2 1,3 2,5 4))',4490),
ST_GeomFromText('MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))',4490),
ST_GeomFromText('Point(2 2)',4490));
insert into t_postgis_0017_02 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(1 1,2 0,3 1))',4490),
ST_GeomFromText('MULTIPOLYGON (((2 0, 3 1, 2 2, 1.5 1.5, 2 1, 1.5 0.5, 2 0)), ((1 0, 1.5 0.5, 1 1, 1.5 1.5, 1 2, 0 1, 1 0)))',4490),
ST_GeomFromText('Point(-5 -9)',4490));


--step3:查看数据   expect:成功
--判断点线是否重叠
select ST_Overlaps(t1.smgeometry3,t2.smgeometry1) from t_postgis_0017_01 t1,t_postgis_0017_02 t2;
--判断点面是否重叠
select ST_Overlaps(t1.smgeometry3,t2.smgeometry2) from t_postgis_0017_01 t1,t_postgis_0017_02 t2;
--判断线面是否重叠
select ST_Overlaps(t1.smgeometry1,t2.smgeometry2) from t_postgis_0017_01 t1,t_postgis_0017_02 t2;
select ST_Overlaps(t2.smgeometry1,t1.smgeometry2) from t_postgis_0017_01 t1,t_postgis_0017_02 t2;
--判断线线是否重叠
select ST_Overlaps(t1.smgeometry1,t2.smgeometry1) from t_postgis_0017_01 t1,t_postgis_0017_02 t2;
--判断面面是否重叠
select ST_Overlaps(t1.smgeometry2,t2.smgeometry2) from t_postgis_0017_01 t1,t_postgis_0017_02 t2;

--step4:清理环境   expect:成功
drop table t_postgis_0017_01 cascade;
drop table t_postgis_0017_02 cascade;
