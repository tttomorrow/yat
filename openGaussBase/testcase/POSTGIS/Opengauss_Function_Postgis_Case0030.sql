-- @testpoint: PostGIS功能覆盖,返回一个线串几何体，且已删除输入几何体在索引位置的点,部分测试点合理报错
-- @description: ST_RemovePoint(geom1,index)，geom1子类型必须为linestring

--step1:创建表   expect:成功
drop table if exists t_postgis_0030;

create table t_postgis_0030 (smgeometry1 geometry(MultiLineString,4490),
                             smgeometry2 geometry(LineString,4490),
                             smgeometry3 geometry(Point,4490),
                             smgeometry4 geometry(MultiPoint,4490));

--step2:插入数据   expect:成功
insert into t_postgis_0030 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(2 1,3 2,5 4))',4490),
ST_GeomFromText('LineString(0 0,1 1,1 2)',4490),
ST_GeomFromText('Point(2 2)',4490),
ST_GeomFromText('MultiPoint((1 1),(2 2))',4490));

--step3:结合表查看数据   expect:成功
--从线串中删除索引位置的点
select ST_AsEWKT(ST_RemovePoint(smgeometry2,0)) from t_postgis_0030;
select ST_AsEWKT(ST_RemovePoint(smgeometry2,1)) from t_postgis_0030;
select ST_AsEWKT(ST_RemovePoint(smgeometry2,2)) from t_postgis_0030;
--查看删除后的数据
select ST_AsEWKT(smgeometry2) from t_postgis_0030;

--报错，索引超出范围
select ST_AsEWKT(ST_RemovePoint(smgeometry2,3)) from t_postgis_0030;

--报错，第一个参数必须是linestring
select ST_AsEWKT(ST_RemovePoint(smgeometry1,0)) from t_postgis_0030;
select ST_AsEWKT(ST_RemovePoint(smgeometry3,0)) from t_postgis_0030;
select ST_AsEWKT(ST_RemovePoint(smgeometry4,0)) from t_postgis_0030;

--step4:清理环境   expect:成功
drop table t_postgis_0030 cascade;

