-- @testpoint: PostGIS功能覆盖，计算geogA与geogB之间的距离,ST_Distance

--step1:创建表   expect:成功
drop table if exists t_postgis_0018_01;
drop table if exists t_postgis_0018_02;
drop table if exists t_postgis_0018_03;

create table t_postgis_0018_01 (smgeometry1 geometry(MultiLineString,4490),
                              smgeometry2 geometry(Polygon,4490),
                              smgeometry3 geometry(Point,4490));
create table t_postgis_0018_02 (smgeometry1 geometry(MultiLineString,4490),
                              smgeometry2 geometry(Polygon,4490),
                              smgeometry3 geometry(Point,4490));
create table t_postgis_0018_03 (distance double precision);

--step2:插入数据   expect:成功
insert into t_postgis_0018_01 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(2 1,3 2,5 4))',4490),
ST_GeomFromText('POLYGON((0 0,4 0,4 4,0 4,0 0))',4490),
ST_GeomFromText('Point(2 2)',4490));
insert into t_postgis_0018_02 values(ST_GeomFromText('MultiLineString((0 0,1 1,1 2),(1 1,2 0,3 1))',4490),
ST_GeomFromText('POLYGON ((-1 0, -3 0, -3 -3, -1 -3, -1 0))',4490),
ST_GeomFromText('Point(-5 -9)',4490));

--step3:查看数据   expect:成功
--计算点点之间的距离
SELECT ST_Distance(t1.smgeometry3,t2.smgeometry3) FROM t_postgis_0018_01 t1,t_postgis_0018_02 t2;
--计算点线之间的距离
SELECT ST_Distance(t1.smgeometry3,t2.smgeometry1) FROM t_postgis_0018_01 t1,t_postgis_0018_02 t2;
SELECT ST_Distance(t2.smgeometry3,t1.smgeometry1) FROM t_postgis_0018_01 t1,t_postgis_0018_02 t2;
--计算点面之间的距离
SELECT ST_Distance(t1.smgeometry3,t2.smgeometry2) FROM t_postgis_0018_01 t1,t_postgis_0018_02 t2;
SELECT ST_Distance(t2.smgeometry3,t1.smgeometry2) FROM t_postgis_0018_01 t1,t_postgis_0018_02 t2;
--计算线面之间的距离
SELECT ST_Distance(t1.smgeometry1,t2.smgeometry2) FROM t_postgis_0018_01 t1,t_postgis_0018_02 t2;
SELECT ST_Distance(t2.smgeometry1,t1.smgeometry2) FROM t_postgis_0018_01 t1,t_postgis_0018_02 t2;
--计算线线之间的距离
SELECT ST_Distance(t1.smgeometry1,t2.smgeometry1) FROM t_postgis_0018_01 t1,t_postgis_0018_02 t2;
--计算面面之间的距离
SELECT ST_Distance(t1.smgeometry2,t2.smgeometry2) FROM t_postgis_0018_01 t1,t_postgis_0018_02 t2;

--将查出来的距离值插入到指定表格的字段中
create or replace procedure p_postgis_0018()
as
sqlstat varchar(200);
begin
    for s1 in select t1.smgeometry2 as a,t2.smgeometry2 as b from t_postgis_0018_01 t1,t_postgis_0018_02 t2 loop
    sqlstat := 'insert into t_postgis_0018_03(distance) values('''||ST_Distance(s1.a,s1.b)||''')';
    execute immediate sqlstat;
    end loop;
    for s2 in select t1.smgeometry3 as a,t2.smgeometry3 as b from t_postgis_0018_01 t1,t_postgis_0018_02 t2 loop
    sqlstat := 'insert into t_postgis_0018_03(distance) values('''||ST_Distance(s2.a,s2.b)||''')';
    execute immediate sqlstat;
    end loop;
    for s3 in select t1.smgeometry3 as a,t2.smgeometry1 as b from t_postgis_0018_01 t1,t_postgis_0018_02 t2 loop
    sqlstat := 'insert into t_postgis_0018_03(distance) values('''||ST_Distance(s3.a,s3.b)||''')';
    execute immediate sqlstat;
    end loop;
end;
/

call p_postgis_0018();
select distance from t_postgis_0018_03;

--step4:清理环境   expect:成功
drop table t_postgis_0018_01 cascade;
drop table t_postgis_0018_02 cascade;
drop table t_postgis_0018_03 cascade;
drop procedure p_postgis_0018;
