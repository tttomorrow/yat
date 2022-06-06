-- @testpoint: PostGIS功能覆盖,插入一个点到线中,ST_AddPoint(geom1,geom2),部分测试点合理报错
-- @description: geom1子类型必须为linestring，geom2子类型必须为point

--step1:创建表   expect:成功
drop table if exists t_postgis_0029;
create table t_postgis_0029 (smgeometry1 geometry(MultiLineString,4490),
                             smgeometry2 geometry(LineString,4490),
                             smgeometry3 geometry(Point,4490),
                             smgeometry4 geometry(MultiPoint,4490));

--step2:插入数据   expect:成功
insert into t_postgis_0029 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(2 1,3 2,5 4))',4490),
ST_GeomFromText('LineString(0 0,1 1,1 2)',4490),
ST_GeomFromText('Point(2 2)',4490),
ST_GeomFromText('MultiPoint((1 1),(2 2))',4490));

--step3:结合表查看数据   expect:成功
select ST_AsEWKT(ST_AddPoint(smgeometry2, smgeometry3)) from t_postgis_0029;
--报错，第一个参数必须是linestring
select ST_AsEWKT(ST_AddPoint(smgeometry1, smgeometry3)) from t_postgis_0029;
--报错，第二个参数必须是point
select ST_AsEWKT(ST_AddPoint(smgeometry2, smgeometry4)) from t_postgis_0029;

--step4:清理环境   expect:成功
drop table t_postgis_0029 cascade;
